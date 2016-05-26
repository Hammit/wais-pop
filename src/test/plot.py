#!/usr/bin/env python2

import argparse
import os.path
import matplotlib.pyplot as plt
import pandas
import glob


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
		df = pandas.read_csv(file, header=None, parse_dates=[0], infer_datetime_format=True)
		dates = df[0]
		col_1 = df[1]
		col_2 = df[2]
		plt.plot(dates, col_1, 'g-', dates, col_2, 'b-')
		plt.show()
