#!/usr/bin/env python2

import sys
import time
from Nonin import *

finished = False

while not finished:
    try:
        # device = Nonin3150.get_device()
        device = sys.argv[1]
        nonin = Nonin3150(device)

        current_time = nonin.get_current_time()
        finished = True

    except Exception:
        time.sleep(1)

print 'Time Information'
print current_time.strftime('   Time on Nonin, GMT: %Y-%m-%d %H:%M:%S UDT')
print current_time.astimezone(tz.tzlocal()).strftime('   Time on Nonin, translated to local timezone: %Y-%m-%d %H:%M:%S%z')

