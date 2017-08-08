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
			check = row[4]
			#print type(row[1])
			if int(check) == 0:
				print "STOP"
				print row
        		sfid = row[1]
			meid = row[2]
			#print row
			if sfid == beforeS and meid == beforeM:
				countRank += 1
				toCompLine = row[5]
				if toCompLine == actual_line:
					all_ranks.append(countRank)
					actual_line = -1

			else:
				if actual_line != -1:
					all_ranks.append(0)
				actual_line = -1
				countRank = 1
				for line in ref_lines:
					if line[0] == sfid and line[1] == meid:
						# Files matched
						actual_line = line[2]
						break
				#print count
				assert actual_line != -1
				beforeS = sfid
				beforeM = meid
				toCompLineD = row[5]
				if toCompLineD == actual_line:
					all_ranks.append(countRank)
					actual_line = -1
			#print row
			#print actual_line
		#print all_ranks
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

		return mean_ranks
		

if __name__ == '__main__':
	file_name = sys.argv[1]
	file_name_two = sys.argv[2]
	javac = create_plot_loc(file_name)
	eclipse = create_plot_loc(file_name_two)
	fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 7), sharey=True)

	ax1.set_title('MRR For JavaC: Error Location')
	ax1.set_ylabel('Reciprocal Rank')		
	ax1.violinplot(javac)
	ax1.set_xticklabels([])
  	ax1.set_xlabel('JavaC')
	#ax1.violinplot(eclipse)
	
	ax2.set_title('MRR For Eclipse: Error Location')
	#ax2.set_ylabel('Reciprocal Rank')		
	ax2.violinplot(eclipse)
	ax2.set_xticklabels([])
  	ax2.set_xlabel('Eclipse')

	plt.show()


