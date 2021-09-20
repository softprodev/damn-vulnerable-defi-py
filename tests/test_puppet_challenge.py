from brownie import (
    accounts,
    Contract,
)
from web3 import Web3

# Uniswap exchange will start with 10 DVT and 10 ETH in liquidity
UNISWAP_INITIAL_TOKEN_RESERVE = Web3.toWei("10", "ether")
UNISWAP_INITIAL_ETH_RESERVE = Web3.toWei("10", "ether")
POOL_INITIAL_TOKEN_BALANCE = Web3.toWei("10000", "ether")
ATTACKER_INITAL_TOKEN_BALANCE = Web3.toWei("100", "ether")


def before():
    # setup scenario
    deployer = accounts[0]
    attacker = accounts[1]
    deployer.transfer("", Web3.toWei("5", "ether"))
    deployer.transfer("", Web3.toWei("5", "ether"))
    deployer.transfer("", Web3.toWei("5", "ether"))

    # Deploy the oracle and setup the trusted sources with initial prices
    oracle_address = TrustfulOracleInitializer.deploy(
        sources,
        ["DVNFT", "DVNFT", "DVNFT"],
        [INITIAL_NFT_PRICE, INITIAL_NFT_PRICE, INITIAL_NFT_PRICE],
        {"from": deployer},
    ).oracle()
    oracle = Contract.from_abi("TrustfulOracle", oracle_address, TrustfulOracle.abi)

    # Deploy the exchange and get the associated ERC721 token
    exchange = Exchange.deploy(
        oracle.address, {"from": deployer, "value": EXCHANGE_INITIAL_ETH_BALANCE}
    )
    token = Contract.from_abi("DamnValuableNFT", exchange.token(), DamnValuableNFT.abi)

    global initial_attacker_balance
    initial_attacker_balance = attacker.balance()


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    # Confirm exchange lost all ETH
    assert Exchange[0].balance() == 0


def test_puppet_challenge():
    before()
    run_exploit()
    after()
