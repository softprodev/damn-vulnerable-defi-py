from brownie import (
    accounts,
    Contract,
    DamnValuableToken,
    FlashLoanerPool,
    TheRewarderPool,
    AccountingToken,
    RewardToken,
)
from web3 import Web3

TOKENS_IN_LENDER_POOL = Web3.toWei("1000000", "ether")

users = []


def before():
    # setup scenario
    deployer = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    charlie = accounts[3]
    david = accounts[4]
    global users
    users = [alice, bob, charlie, david]

    liquidity_token = DamnValuableToken.deploy({"from": deployer})
    flash_loan_pool = FlashLoanerPool.deploy(
        liquidity_token.address, {"from": deployer}
    )

    # Set initial token balance of the pool offering flash loans
    liquidity_token.transfer(
        flash_loan_pool.address, TOKENS_IN_LENDER_POOL, {"from": deployer}
    )

    rewarder_pool = TheRewarderPool.deploy(liquidity_token.address, {"from": deployer})
    global reward_token
    reward_token = Contract.from_abi(
        "RewardToken", rewarder_pool.rewardToken(), RewardToken.abi
    )
    accounting_token = Contract.from_abi(
        "AccountingToken", rewarder_pool.accToken(), AccountingToken.abi
    )

    # Alice, Bob, Charlie, and David deposit 100 tokens each
    amount = Web3.toWei("100", "ether")
    for user in users:
        liquidity_token.transfer(user.address, amount, {"from": deployer})
        liquidity_token.approve(rewarder_pool.address, amount, {"from": user})
        rewarder_pool.deposit(amount, {"from": user})
        assert accounting_token.balanceOf(user.address) == amount

    assert accounting_token.totalSupply() == Web3.toWei("400", "ether")
    assert reward_token.totalSupply() == 0

    # advance time?
    ##
    ## TODO
    ##

    for user in users:
        rewarder_pool.distributeRewards({"from": user})
        assert reward_token.balanceOf(user.address) == 25

    assert reward_token.totalSupply() == Web3.toWei("100", "ether")
    assert TheRewarderPool[0].roundNumber() == 2


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[5] - account to be used for exploit
    pass


def after():
    attacker = accounts[5]

    assert TheRewarderPool[0].roundNumber() == 3
    # Users should not get more rewards this round
    for user in users:
        TheRewarderPool[0].distributeRewards({"from": user})
        assert reward_token.balanceOf(user.address) == 25

    # Rewards must have been issued to the attacker account
    assert reward_token.totalSupply() == Web3.toWei("100", "ether")
    assert reward_token.balanceOf(attacker) > 0


def test_the_rewarder_challenge():
    before()
    run_exploit()
    after()