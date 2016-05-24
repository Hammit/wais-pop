#!/usr/bin/env python2

import matplotlib.pyplot as plt
import pandas
import glob

files = glob.glob('/tmp/wristox-sessions.2.csv')
files.sort()

for file in files:
	df = pandas.read_csv(file, header=None, parse_dates=[0], infer_datetime_format=True)
	dates = df[0]
	col_1 = df[1]
	col_2 = df[2]
	plt.plot(dates, col_1, 'g-', dates, col_2, 'b-')
	plt.show()
