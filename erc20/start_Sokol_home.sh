#!/bin/bash

PARITY_BASE="/home/koal/poa"
TASK="sokol_home"
PARITY_CONFIG="Sokol_home.toml"
TASK_WORK_DIR="${PARITY_BASE}/sokol"

#DEBUG_RPC='-l rpc=trace'
#EXTRA_CONFIG='--jsonrpc-hosts="all" --jsonrpc-cors null'

configdir=`dirname $0`
cd ${configdir}

source start_common.sh
