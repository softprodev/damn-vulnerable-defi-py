from brownie import network, accounts, config

# variables
DECIMALS = 8
STARTING_PRICE = 200000000000

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVINROMENTS = ["development", "ganache-local"]

# Util function to get account depending on network used
def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if id:
        accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVINROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])
