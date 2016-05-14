#!/usr/bin/env python2

from Nonin import *
device = Nonin3150.get_device()
nonin = Nonin3150(device)

sessions = nonin.read_sessions()

