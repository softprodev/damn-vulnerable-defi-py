from brownie import accounts, SideEntranceLenderPool
from web3 import Web3

ETHER_IN_POOL = Web3.toWei("1000", "ether")
ATTACKER_INITIAL_BALANCE = None


def before():
    # setup scenario
    deployer = accounts[0]
    attacker = accounts[1]
    pool = SideEntranceLenderPool.deploy({"from": deployer})
    pool.deposit({"from": deployer, "value": ETHER_IN_POOL})
    assert pool.balance() == ETHER_IN_POOL

    global ATTACKER_INITIAL_BALANCE
    ATTACKER_INITIAL_BALANCE = attacker.balance()


def run_exploit():
    # remove pass and add exploit code here
    # attacker = accounts[1] - account to be used for exploit
    pass


def after():
    attacker = accounts[1]
    assert SideEntranceLenderPool[-1].balance() == 0
    # Not checking exactly how much is the final balance of the attacker,
    # because it'll depend on how much gas the attacker spends in the attack
    # If there were no gas costs, it would be balance before attack + ETHER_IN_POOL
    assert attacker.balance() > ATTACKER_INITIAL_BALANCE


def test_side_entrance_challenge():
    before()
    run_exploit()
    after()
