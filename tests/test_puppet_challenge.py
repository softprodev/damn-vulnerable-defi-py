from brownie import (
    accounts,
    Contract,
    DamnValuableToken,
    PuppetPool,
)
from brownie.network.state import Chain
from decimal import *
from web3 import Web3
import json

# Uniswap exchange will start with 10 DVT and 10 ETH in liquidity
UNISWAP_INITIAL_TOKEN_RESERVE = Web3.toWei("10", "ether")
UNISWAP_INITIAL_ETH_RESERVE = Web3.toWei("10", "ether")
POOL_INITIAL_TOKEN_BALANCE = Web3.toWei("10000", "ether")
ATTACKER_INITAL_TOKEN_BALANCE = Web3.toWei("100", "ether")

ONE_ETH_IN_WEI = Web3.toWei("1", "ether")


def before():
    # setup scenario
    deployer = accounts[0]
    attacker = accounts[1]
    token = DamnValuableToken.deploy({"from": deployer})

    exchange_template = deploy_uniswap_contract("UniswapV1Exchange")
    factory = deploy_uniswap_contract("UniswapV1Factory")

    factory.initializeFactory(exchange_template.address, {"from": deployer})
    exchange_address = factory.createExchange(token.address, {"from": deployer})

    dvt_uniswap_exchange = Contract(
        "DVTUniswapExchange",
        exchange_address.events["NewExchange"]["exchange"],
        exchange_template.abi,
    )

    lending_pool = PuppetPool.deploy(
        token.address, dvt_uniswap_exchange.address, {"from": deployer}
    )
    token.approve(
        dvt_uniswap_exchange.address, UNISWAP_INITIAL_TOKEN_RESERVE, {"from": deployer}
    )

    chain = Chain()
    deadline = chain[-1].timestamp * 2

    dvt_uniswap_exchange.addLiquidity(
        0,
        UNISWAP_INITIAL_TOKEN_RESERVE,
        deadline,
        {"from": deployer, "value": UNISWAP_INITIAL_ETH_RESERVE},
    )

    # ensure Uniswap exchange is working as expected
    assert dvt_uniswap_exchange.getTokenToEthInputPrice(
        ONE_ETH_IN_WEI
    ) == calculate_token_to_eth_input_price(
        ONE_ETH_IN_WEI, UNISWAP_INITIAL_TOKEN_RESERVE, UNISWAP_INITIAL_ETH_RESERVE
    )

    token.transfer(attacker, ATTACKER_INITAL_TOKEN_BALANCE, {"from": deployer})
    token.transfer(lending_pool.address, POOL_INITIAL_TOKEN_BALANCE, {"from": deployer})

    assert lending_pool.computeOraclePrice() == 1

    global initial_attacker_eth_balance
    initial_attacker_eth_balance = attacker.balance()


# Calculates how much ETH (in wei) Uniswap will pay for the given amount of tokens
# Casting it to decimal to pass equality check.
def calculate_token_to_eth_input_price(
    tokens_sold, tokens_in_reserve, ether_in_reserve
):
    return (
        Decimal(tokens_sold)
        * 997
        * ether_in_reserve
        / (tokens_in_reserve * 1000 + tokens_sold * 997)
    )


def deploy_uniswap_contract(file_name):
    with open("build-uniswap-v1\\" + file_name + ".json") as json_file:
        data = json.load(json_file)
        abi = data["abi"]
        bytecode = data["bytecode"]

    # deploys contract
    tx = accounts[0].transfer(data=bytecode)
    return Contract.from_abi(file_name, tx.contract_address, abi)


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    attacker = accounts[1]
    assert (
        DamnValuableToken[0].balanceOf(attacker.address) >= POOL_INITIAL_TOKEN_BALANCE
    )
    assert DamnValuableToken[-1].balanceOf(PuppetPool[-1].address) == 0
    assert attacker.balance() >= initial_attacker_eth_balance


def test_puppet_challenge():
    before()
    run_exploit()
    after()
