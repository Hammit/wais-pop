#!/bin/bash

date=`date +%F`
cd ~
tar -cvzf ~/backup/wais-pop.${date}.tgz bin/ lib/ src/ Documents/

