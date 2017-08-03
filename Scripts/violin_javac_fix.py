# Copyright 2017 Dhvani Patel

from __future__ import division

import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import javalang


def create_plot_fix(file_name):

	ref_lines = []
	with open("/home/dhvani/java-mistakes-data/mistakes.csv", 'rb') as reffile:
		ref_reader = csv.reader(reffile, delimiter=',')
		count = 0
		for line in ref_reader:
			if count != 0:
				ref_lines.append([line[0], line[1], line[5], line[8]])
			count +=1
			

	with open(file_name, 'rb') as csvfile:
   		check_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		beforeS = -1
		beforeM = -1
		actual_line = -1
		countRank = -1
		all_ranks = []
		flagIsDel = False
		for row in check_reader:
			checkType = row[6]
			if checkType == 'd':
				flagIsDel = True
			else:
				flagIsDel = False
			
        		sfid = row[1]
			meid = row[2]
			#print row
			if sfid == beforeS and meid == beforeM:
				countRank += 1
				toCompTok = row[7]
				print toCompTokD
				tokToCompTok = list(javalang.tokenizer.tokenize(toCompTokD))
				print tokToCompTok[0]
				if toCompTok == actual_tok:
					all_ranks.append(countRank)
					actual_tok = ''

			else:
				if actual_line != -1:
					all_ranks.append(0)
				actual_tok = ''
				countRank = 1
				for line in ref_lines:
					if line[0] == sfid and line[1] == meid:
						# Files matched
						if flagIsDel == True:
							actual_tok = line[2]
						else:
							actual_tok = line[3]
						#print actual_tok
						break
				#print count
				#assert actual_tok != ''
				beforeS = sfid
				beforeM = meid
				toCompTokD = row[7]
				# TOKENIZE TOKEN:
				print "HERE"
				print type(toCompTokD)
				tokToCompTok = list(javalang.tokenizer.tokenize("pass"))
				print tokToCompTok[0]
				#print type(radha)
		
	
				if toCompTokD == actual_line:
					all_ranks.append(countRank)
					actual_tok = ''
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


		#ax1 = plt.plot(nrows=1, ncols=1, figsize=(4, 4), sharey=True)

		#ax1.set_title('Default violin plot')
		#ax1.set_ylabel('Observed values')
		plt.violinplot(mean_ranks)
		#plt.subplots_adjust(bottom=0.15, wspace=0.05)
		plt.show()
		

if __name__ == '__main__':
	file_name = sys.argv[1]
	create_plot_fix(file_name)
