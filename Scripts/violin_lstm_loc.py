# Copyright 2017 Dhvani Patel

from __future__ import division

import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np


def create_plot_loc(file_name):

	ref_lines = []
	with open("/home/dhvani/java-mistakes-data/mistakes.csv", 'rb') as reffile:
		ref_reader = csv.reader(reffile, delimiter=',')
		count = 0
		for line in ref_reader:
			if count != 0:
				ref_lines.append([line[0], line[1], line[4]])
			count +=1
			

	with open(file_name, 'rb') as csvfile:
   		check_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		beforeS = -1
		beforeM = -1
		actual_line = -1
		countRank = -1
		all_ranks = []
		for row in check_reader:
			if row[11] != "rank.correct.line":
				all_ranks.append(int(row[11]))
		mean_ranks = []
		from math import log
		for score in all_ranks:
			if score == 0:
				mean_ranks.append(0)
			else:
				mean_ranks.append(1/score)
		print mean_ranks	
		print "Finished"
		sumTot = 0
		for sc in mean_ranks:
			sumTot += sc
		print len(mean_ranks)
		print sumTot/len(mean_ranks)

		
		fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(7, 7), sharey=True)

		ax1.set_title('MRR For LSTM: Location')
		ax1.set_ylabel('Reciprocal Rank')

		
			
		ax1.violinplot(mean_ranks)
		#plax1t.set_xticks([0, 1, 2])
		#plt.set_xticklabels(['A', 'B', 'C'])
		#ax1.set_ylabel('Observed values')
		#plt.subplots_adjust(bottom=0.15, wspace=0.05)
	
		#ax1.get_xaxis().set_tick_params(direction='out')
   		#ax1.xaxis.set_ticks_position('bottom')
   		#ax1.set_xticks(np.arange(1, 1 + 1))
   		#ax1.set_xticklabels(" ")
  		#ax1.set_xlim(0.25, 1 + 0.75)	
		ax1.set_xticklabels([])
  		ax1.set_xlabel('LSTM')

		plt.show()
		

if __name__ == '__main__':
	file_name = sys.argv[1]
	create_plot_loc(file_name)



