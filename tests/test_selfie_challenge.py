from brownie import accounts, DamnValuableTokenSnapshot, SelfiePool, SimpleGovernance
from web3 import Web3

TOKEN_INITIAL_SUPPLY = Web3.toWei("2000000", "ether")
TOKENS_IN_POOL = Web3.toWei("1500000", "ether")


def before():
    # setup scenario
    deployer = accounts[0]
    dvt_token = DamnValuableTokenSnapshot.deploy(
        TOKEN_INITIAL_SUPPLY, {"from": deployer}
    )

    governance = SimpleGovernance.deploy(dvt_token.addres, {"from": deployer})
    pool = SelfiePool.deploy(dvt_token.address, governance.address, {"from": deployer})

    dvt_token.transfer(pool.address, TOKENS_IN_POOL, {"from": deployer})
    assert dvt_token.balanceOf(pool.address) == TOKENS_IN_POOL


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    # Confirm attacker has tokens from pool
    attacker = accounts[1]
    assert DamnValuableTokenSnapshot[0].balanceOf(attacker.address) == TOKENS_IN_POOL
    assert DamnValuableTokenSnapshot[0].balanceOf(SelfiePool[0].address) == 0


def test_selfie_challenge():
    before()
    run_exploit()
    after()
