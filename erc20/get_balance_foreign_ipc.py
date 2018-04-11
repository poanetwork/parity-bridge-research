#!/opt/anaconda3/bin/python 

from web3 import Web3
from toml import load
import sys

test_env_db = '/home/koal/parity/bridge/test_env_db.toml'
try:
    test_env = load(test_env_db)
except:
    sys.exit(1)

bridge_config = load(test_env['bridge_config'])

IPC_file = bridge_config['foreign']['ipc']
web3 = Web3(Web3.IPCProvider(IPC_file))

signer = web3.toChecksumAddress("0xf3ee321df87781864f46f6464e764c2827fca73b")
sender = web3.toChecksumAddress("0x37a30534da3d53aa1867adde26e114a3161b2b12")
#sender = "0x08c7e1b446520914ba7126325d69fe2863f62413"
accounts_list = [signer, sender]

if (len(sys.argv) == 2):
    if (sys.argv[1] == "--all"):
        accounts_list = web3.eth.accounts
    else:
        sys.exit(1)

for i in accounts_list:
    balance=web3.eth.getBalance(i)
    print(i, ":", web3.fromWei(balance, 'ether'))
