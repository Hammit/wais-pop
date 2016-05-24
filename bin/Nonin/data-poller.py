#!/usr/bin/env python2

import re
import sys
import time
import datetime
from Nonin import *

POLL_INTERVAL = 105 # seconds

def csv_filename(device_id=0):
    # device_id can be a dev node like /dev/rfcomm0
    try:
        device_id = int(device_id)

    except ValueError:
        device_id = int(re.sub('^\D+', '', device_id))

    dt = datetime.datetime.now()
    dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S')
    filename = '/home/wais/tmp/wristox-sessions.%d.%s.csv' % (device_id, dt_str)
    return filename


ack_problem = True
nonin = None

while ack_problem:
    try:
        # device = Nonin3150.get_device()
        device = sys.argv[1]
        nonin = Nonin3150(device)
        ack_problem = False

    except Exception:
        ack_problem = True
        time.sleep(1)

# no ack_problem and nonin is now guaranteed to be a valid Nonin3150
while True:
    # Read, Save and Clear session data from the device
    print "Reading data..."
    try:
        sessions = nonin.read_sessions()
        if sessions is not None:
            exporter = Exporter(sessions)
            filename = csv_filename(device_id=device)
            print "Saving session data to %s" % filename
            exporter.export(format='csv', filename=filename)

            print "Clearing device memory"
            nonin.clear_sessions()

            print "Waiting for %d seconds" % POLL_INTERVAL
            time.sleep(POLL_INTERVAL)
    except Exception:
        time.sleep(1)
        print "Exception raised, probably an ACK required"

#import pdb
#pdb.set_trace()
#for session in sessions[0]: print session
#print "Finished!"

