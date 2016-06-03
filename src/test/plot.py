#!/usr/bin/env python2

import argparse
import os.path
import glob
import pandas
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


parser = argparse.ArgumentParser()
parser.add_argument("--csv_file", help="csv file to plot")
parser.add_argument("--csv_files", nargs='+', help="csv files to combine into a single plot")
args = parser.parse_args()


files = []
if args.csv_file:
	files.append(args.csv_file)
elif args.csv_files:
	files = args.csv_files
	files.sort()
else:
	print "No files specified"


for file in files:
	if os.path.getsize(file) > 0:
		# Read the CSV file to plot
		# df = pandas.read_csv(file, header=None, parse_dates=[0])
		df = pandas.read_csv(file, header=None, parse_dates=[0], infer_datetime_format=True)

		# Extract and format data from the datafile
		dates = df[0]
		dates = [datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S') for date in dates]
		col_1 = df[1]
		col_2 = df[2]

		# import pdb
		# pdb.set_trace()
		
		# plt.plot(dates, col_1, 'g-', dates, col_2, 'b-')
		# plt.savefig('/tmp/fig.png')
		# fig.show()

		fig, ax = plt.subplots(1)

		# formatter = mdates.DateFormatter('%d/%m %H:%M:%S')
		# ax.xaxis.set_major_locator(mdates.MinuteLocator())
		# ax.xaxis.set_major_formatter(formatter)

		major_formatter = mdates.DateFormatter('%d/%m %H:%M:%S')
		ax.xaxis.set_major_locator(mdates.AutoDateLocator())
		ax.xaxis.set_major_formatter(major_formatter)

		# minor_formatter = mdates.DateFormatter('%H:%M:%S')
		# ax.xaxis.set_minor_locator(mdates.MinuteLocator())
		# ax.xaxis.set_minor_formatter(minor_formatter)

		ax.plot(dates, col_1, 'g-')
		ax.plot(dates, col_2, 'b-')

		ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
		fig.autofmt_xdate()

		# plt.savefig('/tmp/fig.png')
		plt.show()
