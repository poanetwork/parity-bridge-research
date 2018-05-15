PARITY_EXEC=`which parity`
if [ "${PARITY_EXEC}" == "" ]; then
    PARITY_EXEC=/opt/parity/parity
fi

if [ `ps ax | grep ${PARITY_EXEC} | grep ${PARITY_CONFIG} | wc -l` == "1" ]; then
    echo "Already exists"
    exit 2
fi

if [ `screen -ls ${TASK}.screen | grep ${TASK}.screen | wc -l` == "1" ]; then
    configdir=`dirname $0`
    cd ${configdir}
    exec ${PARITY_EXEC} --config ${PARITY_CONFIG} ${DEBUG_RPC} ${EXTRA_CONFIG}
    exit 1
fi

if [ ! -d ${TASK_WORK_DIR} ]; then
    mkdir -p ${TASK_WORK_DIR}
fi

curdir=`pwd`
scr=$0 

cd ${TASK_WORK_DIR}

exec screen -d -m -U -t "${TASK}" -S "${TASK}.screen" -h 5000 -L -s ${curdir}/${scr}
