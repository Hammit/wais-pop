#!/usr/bin/env python2

import time
import datetime
from Nonin import *

device_id = 2

device = Nonin3150.get_device()
nonin = Nonin3150(device)

# time.sleep(5) # wait for the device to finish changing modes if necessary

dt = datetime.datetime.now()
dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S')

csv_filename = '/tmp/wristox-sessions.%d.%s.csv' % (device_id, dt_str)

sessions = nonin.read_sessions()
exporter = Exporter(sessions)
exporter.export(format='csv', filename=csv_filename)

#import pdb
#pdb.set_trace()
for session in sessions[0]: print session
print "Finished!"
