from brownie import (
    accounts,
    Contract,
    DamnValuableToken,
    PuppetPool,
    UniswapExchange,
    UniswapFactory,
)
from web3 import Web3
from brownie.network.state import Chain

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
    # Deploy token to be traded in Uniswap
    token = DamnValuableToken.deploy({"from": deployer})
    exchange_template = UniswapExchange.deploy(token.address, {"from": deployer})
    uniswap_factory = UniswapFactory.deploy({"from": deployer})

    uniswap_factory.initializeFactory(exchange_template.address, {"from": deployer})
    exchange_address = uniswap_factory.createExchange(token.address, {"from": deployer})
    uniswap_exchange = UniswapExchange.at(exchange_address)

    lending_pool = PuppetPool.deploy(
        token.address, uniswap_exchange.address, {"from": deployer}
    )

    token.approve(
        uniswap_exchange.address, UNISWAP_INITIAL_TOKEN_RESERVE, {"from": deployer}
    )

    chain = Chain()
    deadline = chain[-1].timestamp * 2
    uniswap_exchange.addLiquidity(
        0,
        UNISWAP_INITIAL_TOKEN_RESERVE,
        deadline,
        {"from": deployer, "value": UNISWAP_INITIAL_ETH_RESERVE},
    )

    assert uniswap_exchange.getTokenToEthInputPrice(
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
def calculate_token_to_eth_input_price(
    tokens_sold, tokens_in_reserve, ether_in_reserve
):
    return (
        tokens_sold
        * 997
        * ether_in_reserve
        / (tokens_in_reserve * 1000 + tokens_sold * 997)
    )


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    attacker = accounts[1]
    assert attacker.balance() >= POOL_INITIAL_TOKEN_BALANCE
    assert DamnValuableToken[0].balanceOf(PuppetPool[0].address) == 0
    assert attacker.balance() >= initial_attacker_eth_balance


def test_puppet_challenge():
    before()
    run_exploit()
    after()
