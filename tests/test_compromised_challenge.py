from brownie import (
    accounts,
    Contract,
    DamnValuableNFT,
    Exchange,
    TrustfulOracle,
    TrustfulOracleInitializer,
)
from web3 import Web3

EXCHANGE_INITIAL_ETH_BALANCE = Web3.toWei("10000", "ether")
INITIAL_NFT_PRICE = Web3.toWei("999", "ether")

sources = [
    "0xA73209FB1a42495120166736362A1DfA9F95A105",
    "0xe92401A4d3af5E446d93D11EEc806b1462b39D15",
    "0x81A5D6E50C214044bE44cA0CB057fe119097850c",
]


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


def test_compromised_challenge():
    before()
    run_exploit()
    after()
