#!/usr/bin/env python2

import time
import sys
from Nonin import *

ack_problem = True

while ack_problem:
    try:
        # device = Nonin3150.get_device()
        device = sys.argv[1]
        nonin = Nonin3150(device)

        timeout = 0
        print 'Setting Bluetooth Timeout Period: %d' % timeout
        nonin.set_bluetooth_timeout(timeout)
        ack_problem = False

    except Exception:
        ack_problem = True
        time.sleep(1)

