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
    
        print 'Setting clock on Nonin to current host time...'
        nonin.set_current_time()
    
        ack_problem = False
    
    except Exception:
        ack_problem = True
        time.sleep(1)

