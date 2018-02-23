#!/opt/anaconda3/bin/python

from web3 import Web3
from web3.utils.datastructures import AttributeDict
from toml import load
import json
import sys
import hexbytes

bridge_config = load('/home/koal/parity/bridge/erc20.toml')

_IPC_file = bridge_config['foreign']['ipc']
web3 = Web3(Web3.IPCProvider(_IPC_file))
#web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:48545"))

if (len(sys.argv) == 2):
    txHash = sys.argv[1]
else:
    sys.exit(1)

class ReceiptEncoder(json.JSONEncoder):
     def default(self, obj):
         if type(obj) == hexbytes.HexBytes:
             return obj.hex()
         elif type(obj) == AttributeDict:
             return dict(obj)
         # Let the base class default method raise the TypeError
         return json.JSONEncoder.default(self, obj)

#print(type(dict(web3.eth.getTransactionReceipt(txHash))['blockHash']))
print(json.dumps(dict(web3.eth.getTransactionReceipt(txHash)), cls=ReceiptEncoder, indent=2))
#print(json.dumps(dict(web3.eth.getTransactionReceipt(txHash))))

sys.exit(0)
