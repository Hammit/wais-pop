#!/usr/bin/env python2

import sys, time, datetime
from Nonin import *

finished = False

while not finished:
    try:
		device = sys.argv[1]
		nonin = Nonin3150(device)

		time.sleep(2)

		print 'Attempting to read session data on the device...'
		sessions = nonin.read_sessions()

		dt = datetime.datetime.now()
		dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S')

		csv_filename = '/tmp/wristox-sessions.%d.%s.csv' % (982146, dt_str)

		print 'Exporting data...'
		exporter = Exporter(sessions)
		exporter.export(format='csv', filename=csv_filename)

		finished = True

    except Exception as e:
		print e
		# if nonin:
		# 	nonin.device.close()
		time.sleep(2)


# import pdb
# pdb.set_trace()

# for session in sessions[0]: print session
# print "Finished!"
