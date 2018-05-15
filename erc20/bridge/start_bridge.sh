#!/bin/bash

BRIDGE_BASE="/home/koal/git-repos/parity-bridge-research/erc20/bridge"
TASK="PoA_bridge"
BRIDGE_BIN="./bridge"
CONFIG="sokol_ropsten_config_rpc.toml"
DATABASE="sokol_ropsten_db.toml"

TASK_WORK_DIR="${BRIDGE_BASE}"

if [ `ps ax | grep ${BRIDGE_BIN} | grep ${CONFIG} | wc -l` == "1" ]; then
    echo "Already exists"
    exit 2
fi

if [ `screen -ls ${TASK}.screen | grep ${TASK}.screen | wc -l` == "1" ]; then
    cd ${TASK_WORK_DIR}

    #export RUST_BACKTRACE=1

    #export RUST_LOG=all
    #export RUST_LOG=error
    #export RUST_LOG=warning
    export RUST_LOG=info
    #export RUST_LOG=debug

    exec ${BRIDGE_BIN} --config ${CONFIG} --database ${DATABASE}

    exit 1
fi

curdir=`pwd`
scr=$0 

cd ${TASK_WORK_DIR}

exec screen -d -m -U -t "${TASK}" -S "${TASK}.screen" -h 5000 -L -s ${curdir}/${scr}
