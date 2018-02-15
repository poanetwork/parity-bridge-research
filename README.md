Set of artifacts to investigate behavior of parity-bridge
----

* `./bridge.orig` - artifacts taken and modified from original version of parity-bridge
* `./erc20` - artifacts used to test ability of the bridge to work with ERC20 token

ERC20 token testing
----

The steps below assume that paths corrected in corresponding files.

__The steps below were tested on with Parity 1.9.2 and web3.py 4.0.0b9__

1. run parity (`start_PoA_home.sh` and `start_PoA_foreign.sh`):
   * `PoA_home*` are for the left side of the bridge,
   * `PoA_foreign*` are for the right side of the bridge
   * bridge account for PoA_home: `0x842eb2142c5aa1260954f07aae39ddee1640c3a7`
   * bridge account for PoA_foreign: `0xf3ee321df87781864f46f6464e764c2827fca73b`
   * actor to deposit and withdraw on both sides: `0x37a30534da3d53aa1867adde26e114a3161b2b12`
   * logs are gathered through `screen` facility, so look at `screen.[0,1]` files for logs
   * balances could be get by `erc20/get_balance_home_ipc.py` and `erc20/get_balance_foreign_ipc.py` 
2. run bridge by `erc20/bridge/start_bridge.sh`. Log verbosity could be configured in `erc20/bridge/bridge_runner.sh`. Logs are collected through `screen` facility, so look at the file `screen.[0,1]` for bridge logs.
3. deploy ERC20 token by `erc20/bridge/token/token_foreign.py`. It works with bridge configuration and database files to get information about IPC channels, originator of transactions and the bridge contract.
4. register ERC20 token in the bridge contract by `erc20/bridge/contract/foreign_tokenreg.py`
5. deposit to `HomeBridge` contract by `erc20/bridge/contract/home_deposit.py`. Value of ether to deposit is chosen randomly. 
6. get balance of ERC20 token on the right side by `erc20/bridge/token/token_balance.py`
7. withdraw tokens from tht token contract by `erc20/bridge/token/token_withdraw.py`. Value to withdraw is chosen randomly.
