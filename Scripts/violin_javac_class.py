# Copyright 2017 Dhvani Patel

from __future__ import division

import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import javalang


def create_plot_class(file_name):

	ref_lines = []
	with open("/home/dhvani/java-mistakes-data/mistakes.csv", 'rb') as reffile:
		ref_reader = csv.reader(reffile, delimiter=',')
		count = 0
		for line in ref_reader:
			if count != 0:
				ref_lines.append([line[0], line[1], line[6]])
			count +=1

	with open(file_name, 'rb') as csvfile:
   		check_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		beforeS = -1
		beforeM = -1
		actual_class = '-1'
		countRank = -1
		all_ranks = []
		count = 0
		for row in check_reader:
			#print row
			
        		sfid = row[1]
			meid = row[2]
			#print row
			if sfid == beforeS and meid == beforeM:
				countRank += 1
				toCompClass = row[6]
				if toCompClass == actual_class:
					all_ranks.append(countRank)
					actual_class = '-1'

			else:
				if actual_class != '-1':
					all_ranks.append(0)
				actual_class = '-1'
				countRank = 1
				for line in ref_lines:
					if line[0] == sfid and line[1] == meid:
						# Files matched
						
						actual_class = line[2]
						if actual_class == 'x':
							actual_class = 'd'
						#print actual_tok
						break
				#print count
				assert actual_class != ''
				beforeS = sfid
				beforeM = meid
				toCompClassD = row[6]
				print row
				if toCompClassD == actual_class:
					all_ranks.append(countRank)
					actual_class = '-1'
			#print row
			#print actual_line
		#print all_ranks
		print count
		print len(all_ranks)
		#print type(radha)
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


		#ax1 = plt.plot(nrows=1, ncols=1, figsize=(4, 4), sharey=True)

		#ax1.set_title('Default violin plot')
		#ax1.set_ylabel('Observed values')
		plt.violinplot(mean_ranks)
		#plt.subplots_adjust(bottom=0.15, wspace=0.05)
		plt.show()
		

if __name__ == '__main__':
	file_name = sys.argv[1]
	create_plot_class(file_name)
