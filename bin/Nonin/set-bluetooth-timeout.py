#!/usr/bin/env python2

from Nonin import *
device = Nonin3150.get_device()
nonin = Nonin3150(device)

# Set time on Nonin from laptop, using GMT timezone
current_time = nonin.get_current_time()
print 'Before setting Timeout:'
print current_time.strftime('   Time on Nonin, GMT: %Y-%m-%d %H:%M:%S UDT')
print current_time.astimezone(tz.tzlocal()).strftime('   Time on Nonin, translated to local timezone: %Y-%m-%d %H:%M:%S%z')

timeout = 0
print 'Setting Bluetooth Timeout Period: %d' % timeout
nonin.set_bluetooth_timeout(timeout)
