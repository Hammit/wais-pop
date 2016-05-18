#!/usr/bin/env python2

import time
import datetime
from Nonin import *

def csv_filename(device_id=0):
    dt = datetime.datetime.now()
    dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S')
    filename = '/tmp/wristox-sessions.%d.%s.csv' % (device_id, dt_str)
    return filename

POLL_INTERVAL = 150 # seconds

device = Nonin3150.get_device()
nonin = Nonin3150(device)

# time.sleep(5) # wait for the device to finish changing modes if necessary

while True:
    # Read, Save and Clear session data from the device
    print "Reading data..."
    try:
        sessions = nonin.read_sessions()
        if sessions is not None:
            exporter = Exporter(sessions)
            filename = csv_filename(device_id=2)
            print "Saving session data to %s" % filename
            exporter.export(format='csv', filename=filename)

            print "Clearing device memory"
            nonin.clear_sessions()

            print "Waiting for %d seconds" % POLL_INTERVAL
            time.sleep(POLL_INTERVAL)
    except Exception:
        print "Exception raised, probably an ACK required"

#import pdb
#pdb.set_trace()
for session in sessions[0]: print session
print "Finished!"

