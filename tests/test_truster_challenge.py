from brownie import accounts, DamnValuableToken, TrusterLenderPool
from web3 import Web3

TOKENS_IN_POOL = Web3.toWei("1000000", "ether")


def before():
    # setup scenario
    deployer = accounts[0]
    attacker = accounts[1]
    dvt_token = DamnValuableToken.deploy({"from": deployer})
    lender_pool = TrusterLenderPool.deploy(dvt_token.address, {"from": deployer})
    dvt_token.transfer(lender_pool.address, TOKENS_IN_POOL, {"from": deployer})

    assert dvt_token.balanceOf(lender_pool.address) == TOKENS_IN_POOL
    assert dvt_token.balanceOf(attacker.address) == 0


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    # Confirm attacker has tokens from pool
    attacker = accounts[1]
    assert DamnValuableToken[-1].balanceOf(TrusterLenderPool[0].address) == 0
    assert DamnValuableToken[-1].balanceOf(attacker.address) == TOKENS_IN_POOL


def test_truster_challenge():
    before()
    run_exploit()
    after()
