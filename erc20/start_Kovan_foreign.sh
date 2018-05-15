#!/bin/bash

PARITY_BASE="/home/koal/poa"
TASK="kovan_foreign"
PARITY_CONFIG="Kovan_foreign.toml"
TASK_WORK_DIR="${PARITY_BASE}/kovan"

#DEBUG_RPC='-l rpc=trace'
#EXTRA_CONFIG='--jsonrpc-hosts="all" --jsonrpc-cors null'

configdir=`dirname $0`
cd ${configdir}

source start_common.sh
