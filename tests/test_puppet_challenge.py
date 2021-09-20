from brownie import (
    accounts,
    Contract,
)
from web3 import Web3
import json

# Uniswap exchange will start with 10 DVT and 10 ETH in liquidity
UNISWAP_INITIAL_TOKEN_RESERVE = Web3.toWei("10", "ether")
UNISWAP_INITIAL_ETH_RESERVE = Web3.toWei("10", "ether")
POOL_INITIAL_TOKEN_BALANCE = Web3.toWei("10000", "ether")
ATTACKER_INITAL_TOKEN_BALANCE = Web3.toWei("100", "ether")


def before():
    # setup scenario
    # HOW TO LOAD IN UNISWAP CONTRACTS?
    with open("build-uniswap-v1/UniswapV1Exchange.json", "r") as ex:
        data = json.load(ex)

    # get bytecode
    bytecode = data["bytecode"]
    # get abi
    abi = data["abi"]


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    pass


def test_puppet_challenge():
    before()
    run_exploit()
    after()
