#!/bin/bash

PYTHON='python2'
#
#PATHS="/usr/bin /usr/local/bin /bin"
#BINARIES="python2.7 python2 python"
#
#for path in $PATHS
#do
#    for binary in $BINARIES
#    do
#        echo "${path}/${binary}"
#        if [[ -x "${path}/${binary}" && -z "$PYTHON" ]]
#        then
#            echo found
#            PYTHON="${path}/${binary}"
#            break 2
#        fi
#    done
#done

SELF=`realpath $0`
DIR=`dirname "${SELF}"`
USR="${DIR}/usr"

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${USR}/lib/x86_64-linux-gnu/panda3d/
export PYTHONPATH=${PYTHONPATH}:${USR}/lib/python2.7/dist-packages/:${USR}/lib/python2.7/site-packages/:${USR}/share/panda3d:${USR}/lib/x86_64-linux-gnu/panda3d
echo -e "${USR}/share/panda3d\n${USR}/lib/x86_64-linux-gnu/panda3d" > ${USR}/lib/python2.7/dist-packages/panda3d.pth

echo ${LD_LIBRARY_PATH}
echo ${PYTHONPATH}

cd ${DIR}

${PYTHON} ./test.py
