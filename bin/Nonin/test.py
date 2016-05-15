#!/usr/bin/env python2

from Nonin import *
device = Nonin3150.get_device()
nonin = Nonin3150(device)

import time
time.sleep(1)

import pdb
sessions = nonin.read_sessions()
pdb.set_trace()
for session in sessions[0]: print session
print "Finished!"

