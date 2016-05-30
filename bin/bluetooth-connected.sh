#!/bin/bash

ADDRESS=$1
NAME=$2
SERVICE_NAME=$3
UUID=$4
DEVICE=$5

BIN_PATH=/home/wais/bin/Nonin
DATE=`date +%F`
LIB_PATH=${HOME}/lib/

echo $1,$2,$3,$4,$5 >> ${HOME}/tmp/bluetooth-connected.${DATE}.log

cd $BIN_PATH
sudo PYTHONPATH=$LIB_PATH ${BIN_PATH}/bluetooth-connected.py $ADDRESS $NAME $SERVICE_NAME $UUID $DEVICE

