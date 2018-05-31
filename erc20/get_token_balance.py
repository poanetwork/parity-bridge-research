#!/opt/anaconda3/bin/python

from utils.getenv import BridgeEnv
from sys import argv, exit
from utils.web3 import toChecksumAddress, toEther

direction = "f"
addr_to_get_balance = ""

# The command can be used with 2 parameters:
# #1 - direction (h/f)
# #2 - address to get balance
if len(argv[1:]) in (1, 2):
    if argv[1] in ["h", "f"]:
        direction = argv[1]
    else:
        exit("Incorrect direction")
    if len(argv[1:]) == 2:
        addr_to_get_balance = argv[2]
        if addr_to_get_balance[:2] != "0x":
            addr_to_get_balance = "0x" + addr_to_get_balance
        addr_to_get_balance = toChecksumAddress(addr_to_get_balance)
else:
    if (len(argv) != 1):
        exit("Incorrect number of input parameters")

b = BridgeEnv()
b.initEnv()

if direction == "h":
    web3 = b.connectionToHome()
    b.initHomeBridgeContact()
    b.initHomeTokenContract()
    token_contract = b.home_token
    bridge_address = b.home_bridge_address
else:
    web3 = b.connectionToForeign()
    b.initForeignBridgeContact()
    b.initForeignTokenContract()
    token_contract = b.foreign_token
    bridge_address = b.foreign_bridge_address

if addr_to_get_balance == "":
    addresses = [b.actor_address]
else:
    addresses = [addr_to_get_balance]

for i in addresses:
    balance = token_contract.functions.balanceOf(i).call()
    print(i, ":", toEther(balance))

exit(0)
