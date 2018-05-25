#!/opt/anaconda3/bin/python 

from utils.getenv import BridgeEnv
from utils.web3 import toChecksumAddress
from sys import argv, exit

b = BridgeEnv()
b.initEnv()

signer = b.validator
sender = b.actor_address

# Home direction will be used by default
direction = "h"
if len(argv[1:]) == 1:
    if argv[1] in ["h", "f"]:
        direction = argv[1]
    else:
        exit("Incorrect direction")
else:
    print("Home is used by default")

if direction == "h":
    web3 = b.connectionToHome()
else:
    web3 = b.connectionToForeign()

for i in [signer, sender]:
    balance=web3.eth.getBalance(i)
    print(i, ":", web3.fromWei(balance, 'ether'))
