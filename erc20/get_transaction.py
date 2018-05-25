#!/opt/anaconda3/bin/python

from web3.utils.datastructures import AttributeDict
import json
import hexbytes

from utils.getenv import BridgeEnv
from sys import argv, exit

b = BridgeEnv()
b.initEnv()

if len(argv[1:]) == 2:
    if argv[1] in ["h", "f"]:
        direction = argv[1]
    else:
        exit("Incorrect direction")
    txHash = argv[2]
else:
    exit("h/f for direction and transaction hash are expected")

if direction == "h":
    web3 = b.connectionToHome()
else:
    web3 = b.connectionToForeign()

class ReceiptEncoder(json.JSONEncoder):
     def default(self, obj):
         if type(obj) == hexbytes.HexBytes:
             return obj.hex()
         elif type(obj) == AttributeDict:
             return dict(obj)
         # Let the base class default method raise the TypeError
         return json.JSONEncoder.default(self, obj)

if txHash[:2] != "0x":
    txHash = "0x" + txHash

tx = web3.eth.getTransaction(txHash)
if tx: 
    print(json.dumps(dict(tx), cls=ReceiptEncoder, indent=2))
else:
    exit("Transaction does not exist")

exit(0)
