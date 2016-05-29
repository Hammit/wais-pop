#!/usr/bin/env python2

import sys, time
from Nonin import *

# nonin.enable_logging()

finished = False

while not finished:
    try:
        # device = Nonin3150.get_device()
        device = sys.argv[1]
        nonin = Nonin3150(device)

        config = nonin.get_config()
        for key in config:
            print '{:<27} = {}'.format(key, config[key])

        finished = True

    except Exception:
        time.sleep(2)


import pdb
pdb.set_trace()

print config

