# Copyright 2017 Dhvani Patel

from __future__ import division

import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import javalang
from javac_parser import Java
from io import open

def tokenize(get):
	get = '\'\''
	print get
	tokGen = javalang.tokenizer.tokenize(get + ' ')
	for tok in tokGen:
		print tok


def create_plot_fix(file_name):
	java = Java()
	ref_lines = []
	with open("/home/dhvani/java-mistakes-data/mistakes.csv", 'r') as reffile:
		ref_reader = csv.reader(reffile, delimiter=',')
		count = 0
		for line in ref_reader:
			if count != 0:
				ref_lines.append([line[0], line[1], line[5], line[8]])
			count +=1
			

	with open(file_name, 'r', encoding='utf8') as csvfile:
   		check_reader = csv.reader(csvfile, delimiter=',')
		beforeS = -1
		beforeM = -1
		actual_tok = ''
		countRank = -1
		all_ranks = []
		flagIsDel = False
		for row in check_reader:
			#print row
			checkType = row[7]
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
				
				if toCompTok != '':
					print "----------------------------------"
					print toCompTok
					getToks = java.lex(toCompTok)
					print getToks
					#assert len(getToks) <= 3
					toCompTok = getToks[0][0]
					
					print toCompTok
				
				if toCompTok == actual_tok:
					all_ranks.append(countRank)
					actual_tok = ''

			else:
				if actual_tok != '':
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
				print "ROW"
				print row
				
				toCompTokD = row[7]
				print toCompTokD
				# TOKENIZE TOKEN:
				#print row
				
				if toCompTokD != '':
					print "----------------------------------"
					print toCompTokD
					getToks = java.lex(toCompTokD)
					print getToks
					#assert len(getToks) <= 3
					toCompTokD = getToks[0][0]
					
					print toCompTokD
				print type(radha)
				
				if toCompTokD == actual_tok:
					all_ranks.append(countRank)
					actual_tok = ''
			
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


		fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(7, 7), sharey=True)

		ax1.set_title('MRR For JavaC: Fix Token')
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
  		ax1.set_xlabel('JavaC')

		plt.show()
		

if __name__ == '__main__':
	file_name = sys.argv[1]
	#tokenize(file_name)
	create_plot_fix(file_name)
