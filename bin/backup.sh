#!/bin/bash

BACKUP_DIR=~/backup

date=`date +%F`
if [ ! -d $BACKUP_DIR ]; then mkdir $BACKUP_DIR; fi

backup_filename="${BACKUP_DIR}/wais-pop.${date}.tgz"
tar -chvzf ${backup_filename} -C $HOME bin/ doc/ lib/ src/
