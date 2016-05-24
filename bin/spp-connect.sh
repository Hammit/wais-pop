#!/bin/bash

ADDRESS=$1
NAME=$2
SERVICE_NAME=$3
UUID=$4
DEVICE=$5

DEVICE_ID="2"
DATE=`date +%F`
LIB_PATH=${HOME}/lib/

cd /home/wais/bin/Nonin/
sudo PYTHONPATH=$LIB_PATH ./set-bluetooth-timeout.py $DEVICE
sudo PYTHONPATH=$LIB_PATH ./set-datetime.py $DEVICE
sudo PYTHONPATH=$LIB_PATH ./data-poller.py $DEVICE

#echo $1,$2,$3,$4,$5 >> ${HOME}/tmp/spp-connect.${DATE}.log
