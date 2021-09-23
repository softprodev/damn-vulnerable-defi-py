from brownie import (
    accounts,
    exceptions,
    UnstoppableLender,
    DamnValuableToken,
    ReceiverUnstoppable,
)
from web3 import Web3
import pytest

# Pool has 1M * 10**18 tokens
TOKENS_IN_POOL = Web3.toWei("1000000", "ether")
INITIAL_ATTACKER_BALANCE = Web3.toWei("100", "ether")


def before():
    # Setup scenario
    deployer = accounts[0]
    attacker = accounts[1]
    randomUser = accounts[2]
    dvt_token = DamnValuableToken.deploy({"from": deployer})
    lender = UnstoppableLender.deploy(dvt_token.address, {"from": deployer})

    # approve lender for deployer
    dvt_token.approve(lender.address, TOKENS_IN_POOL, {"from": deployer})
    # setup lender with 1,000,000 DVT
    lender.depositTokens(TOKENS_IN_POOL, {"from": deployer})
    # setup attacker with 100 DVT
    dvt_token.transfer(attacker.address, INITIAL_ATTACKER_BALANCE, {"from": deployer})

    # assert balances and that users can execute flash loans.
    assert dvt_token.balanceOf(lender.address) == TOKENS_IN_POOL
    assert dvt_token.balanceOf(attacker.address) == INITIAL_ATTACKER_BALANCE
    receiver = ReceiverUnstoppable.deploy(lender.address, {"from": randomUser})
    receiver.executeFlashLoan(10, {"from": randomUser})


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    randomUser = accounts[2]
    # Confirm other users now cannot execute flash loans
    with pytest.raises(exceptions.VirtualMachineError):
        ReceiverUnstoppable[-1].executeFlashLoan(10, {"from": randomUser})


def test_unstoppable_challenge():
    before()
    run_exploit()
    after()
