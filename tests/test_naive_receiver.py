from brownie import accounts, exceptions, NaiveReceiverLenderPool, FlashLoanReceiver
from web3 import Web3

# import pytest

ETHER_IN_POOL = Web3.toWei("1000", "ether")
ETHER_IN_RECEIVER = Web3.toWei("10", "ether")


def before():
    # set up contracts
    deployer = accounts[0]
    # attacker = accounts[1]
    random_user = accounts[2]

    lender_pool = NaiveReceiverLenderPool.deploy({"from": deployer})
    deployer.transfer(lender_pool, ETHER_IN_POOL)

    assert lender_pool.balance() == ETHER_IN_POOL
    assert lender_pool.fixedFee({"from": deployer}) == Web3.toWei("1", "ether")

    vulnerable_receiver = FlashLoanReceiver.deploy(
        lender_pool.address, {"from": random_user}
    )
    random_user.transfer(vulnerable_receiver.address, ETHER_IN_RECEIVER)
    assert vulnerable_receiver.balance() == ETHER_IN_RECEIVER


def run_exploit():
    # remove pass and add exploit code here
    pass


def after():
    randomUser = accounts[2]
    assert randomUser.balance() == 0
    assert NaiveReceiverLenderPool[0].balance() == (ETHER_IN_POOL + ETHER_IN_RECEIVER)


def test_naive_receiver():
    before()
    run_exploit()
    after()
