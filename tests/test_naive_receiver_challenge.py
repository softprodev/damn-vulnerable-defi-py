from brownie import (
    accounts,
    NaiveReceiverLenderPool,
    FlashLoanReceiver,
)
from web3 import Web3

# Pool has 1000 ETH in balance
ETHER_IN_POOL = Web3.toWei("1000", "ether")
# Receiver has 10 ETH in balance
ETHER_IN_RECEIVER = Web3.toWei("10", "ether")


def before():
    # Setup scenario
    deployer = accounts[0]
    random_user = accounts[2]

    lender_pool = NaiveReceiverLenderPool.deploy({"from": deployer})
    deployer.transfer(lender_pool, ETHER_IN_POOL)

    assert lender_pool.balance() == ETHER_IN_POOL
    assert lender_pool.fixedFee({"from": deployer}) == Web3.toWei("1", "ether")

    # random_user deploying their flash load receiver
    vulnerable_receiver = FlashLoanReceiver.deploy(
        lender_pool.address, {"from": random_user}
    )
    random_user.transfer(vulnerable_receiver.address, ETHER_IN_RECEIVER)
    assert vulnerable_receiver.balance() == ETHER_IN_RECEIVER


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    # Confirm all ETH has been drained from receiver
    assert FlashLoanReceiver[0].balance() == 0
    assert NaiveReceiverLenderPool[0].balance() == (ETHER_IN_POOL + ETHER_IN_RECEIVER)


def test_naive_receiver_challenge():
    before()
    run_exploit()
    after()
