# Copyright 2017 Dhvani Patel

from keras.models import Sequential
from keras.layers import Dense, Dropout, Input, Embedding, LSTM, Reshape, Flatten, Activation
from keras.models import Model
from keras import optimizers
from keras.callbacks import ModelCheckpoint, CSVLogger, EarlyStopping
from keras import regularizers

import numpy
from Token import Token
from py_mutations_hub import perform
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from itertools import izip_longest
from itertools import izip

import os
import cPickle
import matplotlib.pyplot as plt

import sys

# BATCH = 60
# So 15 of 4 of one window
# One 4:
# [Good, Insert, Delete, Sub]
WINDOW_SIZE = 10

# DEFINED:

# FIXED INPUT BITS = 87 (ONE TOKEN)
# FIXED OUTPUT BITS = 102 (2+2+3+10+85)
# WINDOW = 10, SO BATCH = 40 INPUT, 40 OUTPUT
BATCH_SIZE = 66

def one_hot(indexed_tokens):
	one_hot = []
	nb_classes = 88
	one_hot_targets = np.eye(nb_classes)[indexed_tokens]
	one_hot = one_hot_targets.tolist()
	#print "fort"
	#bruhTemp = one_hot[:]
	for x in range(len(one_hot)):
		#one_hot[x].astype(int)
		[int(i) for i in one_hot[x]]
	#one_hot.astype(int)
	#print type(one_hot[0][0])
	return one_hot

def getInputTen(allTrainData):
	#one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(0)
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = one_hot(allTrainData[0][0]),one_hot(allTrainData[0][1]), one_hot(allTrainData[0][2]), one_hot(allTrainData[0][3])
	while(one_hot_good == 1):
			one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = one_hot(allTrainData[0][0]),one_hot(allTrainData[0][1]), one_hot(allTrainData[0][2]), one_hot(allTrainData[0][3])
	#print type(one_hot_good)
	#print one_hot_good
	windowInd = 0
	fileInd = 0
	batchInd = 1
	#count = 0
	while True: # 462540
	#while windowInd < int(len(insArr)/10):
		if fileInd >= 1000:
			fileInd = 0
		#print "file"
		#print fileInd
		#print minSize
		#print windowInd
		#print int((int(minSize) / 10))

		loopInd = 0
		batchArr = []
		while loopInd < (BATCH_SIZE / 3):
			sizes = [len(one_hot_good), len(one_hot_bad_ins),len(one_hot_bad_del),len(one_hot_bad_sub)]
			minSize = min(float(siz) for siz in sizes) # min of a generator
			if windowInd < int((int(minSize) - 10)):
				#print windowInd
				#print "WINDOW"	
				batchInd = 1
			
				#print len(one_hot_good)
				#print len(one_hot_bad_ins)
				#print len(one_hot_bad_del)
				#print len(one_hot_bad_sub)	
				toPassOne = []
				for x in range(10):
					y = x + windowInd
					if y < len(one_hot_good):
						toPassOne.append(one_hot_good[y])
				toPassTwo = []	
				for x in range(10):
					y = x + windowInd
					if y < len(one_hot_bad_ins):
						toPassTwo.append(one_hot_bad_ins[y])
				toPassThree = []	
				for x in range(10):
					y = x + windowInd
					if y < len(one_hot_bad_del):				
						toPassThree.append(one_hot_bad_del[y])
				toPassFour = []
				for x in range(10):
					y = x + windowInd
					if y < len(one_hot_bad_sub):	
						toPassFour.append(one_hot_bad_sub[y])
			#print "TEST"
			#print numpy.array(toPassOne).astype(int)[0]
			#print len(toPass)
			#print len(toPassOne)
			#print len(toPassTwo)
			#print len(toPassThree)
			#print len(toPassFour)
			
			#toPass = np.array((,, ))

			#toPass = np.concatenate((numpy.array(toPassOne).astype(int),  numpy.array(toPassTwo).astype(int), numpy.array(toPassThree).astype(int)), axis=0)
			#a = numpy.array(toPass).astype(int)
			#print toPass.shape
			#toPass = []
			
				while(batchInd % 4 != 0):
					toPass = []
					#print "BATCH IND"
					#print batchInd
					if(batchInd == 1):
						toPass = toPassOne[:]
					elif(batchInd == 2):
						toPass = toPassTwo[:]
					elif(batchInd == 3):
						toPass = toPassThree[:]
					elif(batchInd == 4):
						print "here"
						toPass = toPassTwo[:]
					#print toPass
					#print [toPass]
					a = numpy.array(toPass).astype(int)
					#print a.shape
					#count+=1
					#print "COUNT"
					#print count
					#print b.shape
					#print a
					batchArr.append(a)
					batchInd += 1
			
				#print numpy.array(toPass).shape
				#print "mine too"
				#a = numpy.array(toPass)
				#print a.shape
				#yield a
				windowInd += 1
				#print loopInd
				loopInd += 1
			else:
				old_one_hot_good = one_hot_good[:]
				old_one_hot_bad_ins = one_hot_bad_ins[:]
				old_one_hot_bad_del = one_hot_bad_del[:]
				old_one_hot_bad_sub = one_hot_bad_sub[:]

				numGoodLeft = len(one_hot_good) % 10
				numBadInsLeft = len(one_hot_bad_ins) % 10
				numBadDelLeft = len(one_hot_bad_del) % 10
				numBadSubLeft = len(one_hot_bad_sub) % 10

				fileInd += 1
				if fileInd >= 1000:
					fileInd = 0
				#print "FILE IND"
				#print fileInd
				windowInd = 0
				#one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(fileInd)
				one_hot_good = allTrainData[fileInd]
				while(one_hot_good == -1):
					fileInd+=1
					one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = one_hot(allTrainData[fileInd][0]),one_hot(allTrainData[fileInd][1]), one_hot(allTrainData[fileInd][2]), one_hot(allTrainData[fileInd][3])
				if one_hot_good != -1:
					one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = one_hot(allTrainData[fileInd][0]),one_hot(allTrainData[fileInd][1]), one_hot(allTrainData[fileInd][2]), one_hot(allTrainData[fileInd][3])
	
			
				for p in range(numGoodLeft):
					one_hot_good.insert(p, old_one_hot_good[len(old_one_hot_good)-numGoodLeft+p])
				for p in range(numBadInsLeft):
					one_hot_bad_ins.insert(p, old_one_hot_bad_ins[len(old_one_hot_bad_ins)-numBadInsLeft+p])
				for p in range(numBadDelLeft):
					one_hot_bad_del.insert(p, old_one_hot_bad_del[len(old_one_hot_bad_del)-numBadDelLeft+p])
				for p in range(numBadSubLeft):
					one_hot_bad_sub.insert(p, old_one_hot_bad_sub[len(old_one_hot_bad_sub)-numBadSubLeft+p])

		#print numpy.array(batchArr).shape
		#print len(batchArr)
		#print "dhvani"
		b = numpy.array(batchArr)
		#print b.shape
		yield b
			
				
		#else:
		#print "NEXT FILE"
		#print "DONE BRO"

		'''
		old_one_hot_good = one_hot_good[:]
		old_one_hot_bad_ins = one_hot_bad_ins[:]
		old_one_hot_bad_del = one_hot_bad_del[:]
		old_one_hot_bad_sub = one_hot_bad_sub[:]

		numGoodLeft = len(one_hot_good) % 10
		numBadInsLeft = len(one_hot_bad_ins) % 10
		numBadDelLeft = len(one_hot_bad_del) % 10
		numBadSubLeft = len(one_hot_bad_sub) % 10

		fileInd += 1
		print "FILE IND"
		print fileInd
		windowInd = 0
		one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(fileInd)
		while(one_hot_good == 1):
			fileInd+=1
			one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(fileInd)
	
			
		for p in range(numGoodLeft):
			one_hot_good.insert(p, old_one_hot_good[len(old_one_hot_good)-numGoodLeft+p])
		for p in range(numBadInsLeft):
			one_hot_bad_ins.insert(p, old_one_hot_bad_ins[len(old_one_hot_bad_ins)-numBadInsLeft+p])
		for p in range(numBadDelLeft):
			one_hot_bad_del.insert(p, old_one_hot_bad_del[len(old_one_hot_bad_del)-numBadDelLeft+p])
		for p in range(numBadSubLeft):
			one_hot_bad_sub.insert(p, old_one_hot_bad_sub[len(old_one_hot_bad_sub)-numBadSubLeft+p])
		'''

def getOutputTen(allTrainData):
	#_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out, _ = perform(0)
	one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = one_hot(allTrainData[0][0]),one_hot(allTrainData[0][1]), one_hot(allTrainData[0][2]), one_hot(allTrainData[0][3])
	
	while(one_hot_good_out == 1):
			#_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out, _ = perform(0)
			one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = one_hot(allTrainData[0][0]),one_hot(allTrainData[0][1]), one_hot(allTrainData[0][2]), one_hot(allTrainData[0][3])
	#print type(one_hot_good_out)
	#print one_hot_good_out
	windowInd = 0
	fileInd = 0
	batchInd = 1
	while True: # 462540
	#while windowInd < int(len(insArr)/10):
		if fileInd >= 1000:
			fileInd = 0

		loopInd = 0
		batchArr = []
		while loopInd < (BATCH_SIZE / 3):
			sizes = [len(one_hot_good_out), len(one_hot_bad_ins_out),len(one_hot_bad_del_out),len(one_hot_bad_sub_out)]
			minSize = min(float(siz) for siz in sizes) # min of a generator
			if windowInd < int((int(minSize)-10)):	
				batchInd = 1	
				toPassOne = []
				#for x in range(10):
				y = windowInd
				if y < len(one_hot_good_out):
					err = one_hot_good_out[y][0]
					clasF = one_hot_good_out[y][4]
					clasF = one_hot_good_out[y][5]	
					clasF = one_hot_good_out[y][6]
					#bruhOne = []
					if True:
						zero = 1
						toPassOne.append(zero)
						one = 0
						toPassOne.append(one)
						two = 0
						toPassOne.append(two)
						three = 0
						toPassOne.append(three)
					else:
						print "not here"
					#toPassOne.append(bruhOne)
					#print bruhOne
				#print "TO PASS"
				#print toPassOne
				toPassTwo = []
				#for x in range(10):
				y = windowInd
				if y < len(one_hot_bad_ins_out):
					err = one_hot_bad_ins_out[y][0]
					clasF = one_hot_bad_ins_out[y][4]
					clasF = one_hot_bad_ins_out[y][5]	
					clasF = one_hot_bad_ins_out[y][6]
					#bruhTwo = []
					if True:
						zero = 0
						toPassTwo.append(zero)
						one = 0
						toPassTwo.append(one)
						two = 0
						toPassTwo.append(two)
						three = 1
						toPassTwo.append(three)
					else:
						print "GET OUT OF HERE"
						print type(radha)
					#toPassTwo.append(bruhTwo)
				toPassThree = []
				#for x in range(10):
				y = windowInd
				if y < len(one_hot_bad_del_out):
					#toPassThree.append(one_hot_bad_del_out[y])
					err = one_hot_bad_del_out[y][0]
					clasF = one_hot_bad_del_out[y][4]
					clasF = one_hot_bad_del_out[y][5]	
					clasF = one_hot_bad_del_out[y][6]
					#bruhThree = []
					if True:
						zero = 0
						toPassThree.append(zero)
						one = 0
						toPassThree.append(one)
						two = 1
						toPassThree.append(two)
						three = 0
						toPassThree.append(three)
					else:
						print "GET OUT OF HERE"
						print type(radha)
					#toPassThree.append(bruhThree)
				toPassFour = []
				#for x in range(10):
				y = windowInd
				if y < len(one_hot_bad_sub_out):
					#toPassFour.append(one_hot_bad_sub_out[y])
					err = one_hot_bad_sub_out[y][0]
					clasF = one_hot_bad_sub_out[y][4]
					clasF = one_hot_bad_sub_out[y][5]	
					clasF = one_hot_bad_sub_out[y][6]
					#bruhFour = []
					if True:
						zero = 0
						toPassFour.append(zero)
						one = 1
						toPassFour.append(one)
						two = 0
						toPassFour.append(two)
						three = 0
						toPassFour.append(three)
					else:
						zero = 1
						toPassFour.append(zero)
						one = 0
						toPassFour.append(one)
						two = 0
						toPassFour.append(two)
						three = 0
						toPassFour.append(three)
					#toPassFour.append(bruhFour)
				#print "TEST OUT"
				#print toPassOne[0]
				#print len(toPass)
				#toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
				#print toPass.shape
			
				while(batchInd % 4 != 0):
					toPass = []
					#print "BATCH IND"
					#print batchInd
					if(batchInd == 1):
						toPass = toPassOne[:]
					elif(batchInd == 2):
						toPass = toPassTwo[:]
					elif(batchInd == 3):
						toPass = toPassThree[:]
					elif(batchInd == 4):
						print "here"
						toPass = toPassTwo[:]
					#print len(toPass)
					#print toPassOne[1]
					a = numpy.array(toPass)
					#a = b[None, :]
					#print a.shape
					#print numpy.array(toPassOne)
					#print a
					#count+=1
					#print "COUNT"
					#print count
					#print b.shape	
					#print a
					#yield a
					batchArr.append(a)
					batchInd += 1
					#toPass = np.concatenate((numpy.array(toPassOne).astype(int),  numpy.array(toPassTwo).astype(int), numpy.array(toPassThree).astype(int)), axis=0)	
					#a = numpy.array(toPass)
					#yield a
				windowInd += 1
				#print loopInd
				loopInd += 1
			else:

				#print "NEXT FILE"
	
				#old_one_hot_good_out = one_hot_good_out[:]
				#old_one_hot_bad_ins_out = one_hot_bad_ins_out[:]
				#old_one_hot_bad_del_out = one_hot_bad_del_out[:]
				#old_one_hot_bad_sub_out = one_hot_bad_sub_out[:]

				#numGoodOutLeft = len(one_hot_good_out) % 10
				#numBadInsOutLeft = len(one_hot_bad_ins_out) % 10
				#numBadDelOutLeft = len(one_hot_bad_del_out) % 10
				#numBadSubOutLeft = len(one_hot_bad_sub_out) % 10

				fileInd += 1
				if fileInd >= 1000:
					fileInd = 0
				windowInd = 0
				#_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out, _ = perform(fileInd)
				print fileInd
				#print allTrainData[37]
				#print type(allTrainData[fileInd][1])
				#print type(allTrainData[fileInd][2])
				#print type(allTrainData[fileInd][3])


				one_hot_good_out = allTrainData[fileInd]
				while(one_hot_good_out == -1):
					fileInd+=1
					#_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out, _ = perform(fileInd)
					one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = one_hot(allTrainData[fileInd][0]),one_hot(allTrainData[fileInd][1]), one_hot(allTrainData[fileInd][2]), one_hot(allTrainData[fileInd][3])


				if one_hot_good_out != -1:
					one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = one_hot(allTrainData[fileInd][0]),one_hot(allTrainData[fileInd][1]), one_hot(allTrainData[fileInd][2]), one_hot(allTrainData[fileInd][3])

				#for p in range(numGoodOutLeft):
				#	one_hot_good_out.insert(p, old_one_hot_good_out[len(old_one_hot_good_out)-numGoodOutLeft+p])
				#for p in range(numBadInsOutLeft):
				#	one_hot_bad_ins_out.insert(p, old_one_hot_bad_ins_out[len(old_one_hot_bad_ins_out)-numBadInsOutLeft+p])
				#for p in range(numBadDelOutLeft):
				#	one_hot_bad_del_out.insert(p, old_one_hot_bad_del_out[len(old_one_hot_bad_del_out)-numBadDelOutLeft+p])
				#for p in range(numBadSubOutLeft):
				#	one_hot_bad_sub_out.insert(p, old_one_hot_bad_sub_out[len(old_one_hot_bad_sub_out)-numBadSubOutLeft+p])
			#print loopInd
			#loopInd += 1
		#print numpy.array(batchArr).shape
		#print len(batchArr)
		#print "dhvani"
		b = numpy.array(batchArr)
		#print b.shape
		yield b


def getInputValTen(allValData):
	#one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(0)
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = one_hot(allValData[0][0]),one_hot(allValData[0][1]), one_hot(allValData[0][2]), one_hot(allValData[0][3])
	while(one_hot_good == 1):
			one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = one_hot(allValData[0][0]),one_hot(allValData[0][1]), one_hot(allValData[0][2]), one_hot(allValData[0][3])
	#print type(one_hot_good)
	#print one_hot_good
	windowInd = 0
	fileInd = 0
	batchInd = 1
	#count = 0
	while True: # 462540
	#while windowInd < int(len(insArr)/10):
		if fileInd >= 1000:
			fileInd = 0
		#print "file"
		#print fileInd
		#print minSize
		#print windowInd
		#print int((int(minSize) / 10))

		loopInd = 0
		batchArr = []
		while loopInd < (BATCH_SIZE / 3):
			sizes = [len(one_hot_good), len(one_hot_bad_ins),len(one_hot_bad_del),len(one_hot_bad_sub)]
			minSize = min(float(siz) for siz in sizes) # min of a generator
			if windowInd < int((int(minSize) - 10)):
				#print windowInd
				#print "WINDOW"	
				batchInd = 1
			
				#print len(one_hot_good)
				#print len(one_hot_bad_ins)
				#print len(one_hot_bad_del)
				#print len(one_hot_bad_sub)	
				toPassOne = []
				for x in range(10):
					y = x + windowInd
					if y < len(one_hot_good):
						toPassOne.append(one_hot_good[y])
				toPassTwo = []	
				for x in range(10):
					y = x + windowInd
					if y < len(one_hot_bad_ins):
						toPassTwo.append(one_hot_bad_ins[y])
				toPassThree = []	
				for x in range(10):
					y = x + windowInd
					if y < len(one_hot_bad_del):				
						toPassThree.append(one_hot_bad_del[y])
				toPassFour = []
				for x in range(10):
					y = x + windowInd
					if y < len(one_hot_bad_sub):	
						toPassFour.append(one_hot_bad_sub[y])
			#print "TEST"
			#print numpy.array(toPassOne).astype(int)[0]
			#print len(toPass)
			#print len(toPassOne)
			#print len(toPassTwo)
			#print len(toPassThree)
			#print len(toPassFour)
			
			#toPass = np.array((,, ))

			#toPass = np.concatenate((numpy.array(toPassOne).astype(int),  numpy.array(toPassTwo).astype(int), numpy.array(toPassThree).astype(int)), axis=0)
			#a = numpy.array(toPass).astype(int)
			#print toPass.shape
			#toPass = []
			
				while(batchInd % 4 != 0):
					toPass = []
					#print "BATCH IND"
					#print batchInd
					if(batchInd == 1):
						toPass = toPassOne[:]
					elif(batchInd == 2):
						toPass = toPassTwo[:]
					elif(batchInd == 3):
						toPass = toPassThree[:]
					elif(batchInd == 4):
						print "here"
						toPass = toPassTwo[:]
					#print toPass
					#print [toPass]
					a = numpy.array(toPass).astype(int)
					#print a.shape
					#count+=1
					#print "COUNT"
					#print count
					#print b.shape
					#print a
					batchArr.append(a)
					batchInd += 1
			
				#print numpy.array(toPass).shape
				#print "mine too"
				#a = numpy.array(toPass)
				#print a.shape
				#yield a
				windowInd += 1
				#print loopInd
				loopInd += 1
			else:
				old_one_hot_good = one_hot_good[:]
				old_one_hot_bad_ins = one_hot_bad_ins[:]
				old_one_hot_bad_del = one_hot_bad_del[:]
				old_one_hot_bad_sub = one_hot_bad_sub[:]

				numGoodLeft = len(one_hot_good) % 10
				numBadInsLeft = len(one_hot_bad_ins) % 10
				numBadDelLeft = len(one_hot_bad_del) % 10
				numBadSubLeft = len(one_hot_bad_sub) % 10

				fileInd += 1
				if fileInd >= 1000:
					fileInd = 0
				#print "FILE IND"
				#print fileInd
				windowInd = 0
				#one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(fileInd)
				one_hot_good = allValData[fileInd]
				while(one_hot_good == -1):
					fileInd+=1
					one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = one_hot(allValData[fileInd][0]),one_hot(allValData[fileInd][1]), one_hot(allValData[fileInd][2]), one_hot(allValData[fileInd][3])
				if one_hot_good != -1:
					one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = one_hot(allValData[fileInd][0]),one_hot(allValData[fileInd][1]), one_hot(allValData[fileInd][2]), one_hot(allValData[fileInd][3])
	
			
				for p in range(numGoodLeft):
					one_hot_good.insert(p, old_one_hot_good[len(old_one_hot_good)-numGoodLeft+p])
				for p in range(numBadInsLeft):
					one_hot_bad_ins.insert(p, old_one_hot_bad_ins[len(old_one_hot_bad_ins)-numBadInsLeft+p])
				for p in range(numBadDelLeft):
					one_hot_bad_del.insert(p, old_one_hot_bad_del[len(old_one_hot_bad_del)-numBadDelLeft+p])
				for p in range(numBadSubLeft):
					one_hot_bad_sub.insert(p, old_one_hot_bad_sub[len(old_one_hot_bad_sub)-numBadSubLeft+p])

		#print numpy.array(batchArr).shape
		#print len(batchArr)
		#print "dhvani"
		b = numpy.array(batchArr)
		#print b.shape
		yield b
			
				
		#else:
		#print "NEXT FILE"
		#print "DONE BRO"

		'''
		old_one_hot_good = one_hot_good[:]
		old_one_hot_bad_ins = one_hot_bad_ins[:]
		old_one_hot_bad_del = one_hot_bad_del[:]
		old_one_hot_bad_sub = one_hot_bad_sub[:]

		numGoodLeft = len(one_hot_good) % 10
		numBadInsLeft = len(one_hot_bad_ins) % 10
		numBadDelLeft = len(one_hot_bad_del) % 10
		numBadSubLeft = len(one_hot_bad_sub) % 10

		fileInd += 1
		print "FILE IND"
		print fileInd
		windowInd = 0
		one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(fileInd)
		while(one_hot_good == 1):
			fileInd+=1
			one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(fileInd)
	
			
		for p in range(numGoodLeft):
			one_hot_good.insert(p, old_one_hot_good[len(old_one_hot_good)-numGoodLeft+p])
		for p in range(numBadInsLeft):
			one_hot_bad_ins.insert(p, old_one_hot_bad_ins[len(old_one_hot_bad_ins)-numBadInsLeft+p])
		for p in range(numBadDelLeft):
			one_hot_bad_del.insert(p, old_one_hot_bad_del[len(old_one_hot_bad_del)-numBadDelLeft+p])
		for p in range(numBadSubLeft):
			one_hot_bad_sub.insert(p, old_one_hot_bad_sub[len(old_one_hot_bad_sub)-numBadSubLeft+p])
		'''

def getOutputValTen(allValData):
	#_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out, _ = perform(0)
	one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = one_hot(allValData[0][0]),one_hot(allValData[0][1]), one_hot(allValData[0][2]), one_hot(allValData[0][3])
	
	while(one_hot_good_out == 1):
			#_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out, _ = perform(0)
			one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = one_hot(allValData[0][0]),one_hot(allValData[0][1]), one_hot(allValData[0][2]), one_hot(allValData[0][3])
	#print type(one_hot_good_out)
	#print one_hot_good_out
	windowInd = 0
	fileInd = 0
	batchInd = 1
	while True: # 462540
	#while windowInd < int(len(insArr)/10):
		if fileInd >= 1000:
			fileInd = 0

		loopInd = 0
		batchArr = []
		while loopInd < (BATCH_SIZE / 3):
			sizes = [len(one_hot_good_out), len(one_hot_bad_ins_out),len(one_hot_bad_del_out),len(one_hot_bad_sub_out)]
			minSize = min(float(siz) for siz in sizes) # min of a generator
			if windowInd < int((int(minSize)-10)):	
				batchInd = 1	
				toPassOne = []
				#for x in range(10):
				y = windowInd
				if y < len(one_hot_good_out):
					err = one_hot_good_out[y][0]
					clasF = one_hot_good_out[y][4]
					clasF = one_hot_good_out[y][5]	
					clasF = one_hot_good_out[y][6]
					#bruhOne = []
					if True:
						zero = 1
						toPassOne.append(zero)
						one = 0
						toPassOne.append(one)
						two = 0
						toPassOne.append(two)
						three = 0
						toPassOne.append(three)
					else:
						print "not here"
					#toPassOne.append(bruhOne)
					#print bruhOne
				#print "TO PASS"
				#print toPassOne
				toPassTwo = []
				#for x in range(10):
				y = windowInd
				if y < len(one_hot_bad_ins_out):
					err = one_hot_bad_ins_out[y][0]
					clasF = one_hot_bad_ins_out[y][4]
					clasF = one_hot_bad_ins_out[y][5]	
					clasF = one_hot_bad_ins_out[y][6]
					#bruhTwo = []
					if True:
						zero = 0
						toPassTwo.append(zero)
						one = 0
						toPassTwo.append(one)
						two = 0
						toPassTwo.append(two)
						three = 1
						toPassTwo.append(three)
					else:
						print "GET OUT OF HERE"
						print type(radha)
					#toPassTwo.append(bruhTwo)
				toPassThree = []
				#for x in range(10):
				y = windowInd
				if y < len(one_hot_bad_del_out):
					#toPassThree.append(one_hot_bad_del_out[y])
					err = one_hot_bad_del_out[y][0]
					clasF = one_hot_bad_del_out[y][4]
					clasF = one_hot_bad_del_out[y][5]	
					clasF = one_hot_bad_del_out[y][6]
					#bruhThree = []
					if True:
						zero = 0
						toPassThree.append(zero)
						one = 0
						toPassThree.append(one)
						two = 1
						toPassThree.append(two)
						three = 0
						toPassThree.append(three)
					else:
						print "GET OUT OF HERE"
						print type(radha)
					#toPassThree.append(bruhThree)
				toPassFour = []
				#for x in range(10):
				y = windowInd
				if y < len(one_hot_bad_sub_out):
					#toPassFour.append(one_hot_bad_sub_out[y])
					err = one_hot_bad_sub_out[y][0]
					clasF = one_hot_bad_sub_out[y][4]
					clasF = one_hot_bad_sub_out[y][5]	
					clasF = one_hot_bad_sub_out[y][6]
					#bruhFour = []
					if True:
						zero = 0
						toPassFour.append(zero)
						one = 1
						toPassFour.append(one)
						two = 0
						toPassFour.append(two)
						three = 0
						toPassFour.append(three)
					else:
						zero = 1
						toPassFour.append(zero)
						one = 0
						toPassFour.append(one)
						two = 0
						toPassFour.append(two)
						three = 0
						toPassFour.append(three)
					#toPassFour.append(bruhFour)
				#print "TEST OUT"
				#print toPassOne[0]
				#print len(toPass)
				#toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
				#print toPass.shape
			
				while(batchInd % 4 != 0):
					toPass = []
					#print "BATCH IND"
					#print batchInd
					if(batchInd == 1):
						toPass = toPassOne[:]
					elif(batchInd == 2):
						toPass = toPassTwo[:]
					elif(batchInd == 3):
						toPass = toPassThree[:]
					elif(batchInd == 4):
						print "here"
						toPass = toPassTwo[:]
					#print len(toPass)
					#print toPassOne[1]
					a = numpy.array(toPass)
					#a = b[None, :]
					#print a.shape
					#print numpy.array(toPassOne)
					#print a
					#count+=1
					#print "COUNT"
					#print count
					#print b.shape	
					#print a
					#yield a
					batchArr.append(a)
					batchInd += 1
					#toPass = np.concatenate((numpy.array(toPassOne).astype(int),  numpy.array(toPassTwo).astype(int), numpy.array(toPassThree).astype(int)), axis=0)	
					#a = numpy.array(toPass)
					#yield a
				windowInd += 1
				#print loopInd
				loopInd += 1
			else:

				#print "NEXT FILE"
	
				#old_one_hot_good_out = one_hot_good_out[:]
				#old_one_hot_bad_ins_out = one_hot_bad_ins_out[:]
				#old_one_hot_bad_del_out = one_hot_bad_del_out[:]
				#old_one_hot_bad_sub_out = one_hot_bad_sub_out[:]

				#numGoodOutLeft = len(one_hot_good_out) % 10
				#numBadInsOutLeft = len(one_hot_bad_ins_out) % 10
				#numBadDelOutLeft = len(one_hot_bad_del_out) % 10
				#numBadSubOutLeft = len(one_hot_bad_sub_out) % 10

				fileInd += 1
				if fileInd >= 1000:
					fileInd = 0
				windowInd = 0
				#_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out, _ = perform(fileInd)
				print fileInd
				#print allValData[37]
				#print type(allValData[fileInd][1])
				#print type(allValData[fileInd][2])
				#print type(allValData[fileInd][3])


				one_hot_good_out = allValData[fileInd]
				while(one_hot_good_out == -1):
					fileInd+=1
					#_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out, _ = perform(fileInd)
					one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = one_hot(allValData[fileInd][0]),one_hot(allValData[fileInd][1]), one_hot(allValData[fileInd][2]), one_hot(allValData[fileInd][3])


				if one_hot_good_out != -1:
					one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = one_hot(allValData[fileInd][0]),one_hot(allValData[fileInd][1]), one_hot(allValData[fileInd][2]), one_hot(allValData[fileInd][3])

				#for p in range(numGoodOutLeft):
				#	one_hot_good_out.insert(p, old_one_hot_good_out[len(old_one_hot_good_out)-numGoodOutLeft+p])
				#for p in range(numBadInsOutLeft):
				#	one_hot_bad_ins_out.insert(p, old_one_hot_bad_ins_out[len(old_one_hot_bad_ins_out)-numBadInsOutLeft+p])
				#for p in range(numBadDelOutLeft):
				#	one_hot_bad_del_out.insert(p, old_one_hot_bad_del_out[len(old_one_hot_bad_del_out)-numBadDelOutLeft+p])
				#for p in range(numBadSubOutLeft):
				#	one_hot_bad_sub_out.insert(p, old_one_hot_bad_sub_out[len(old_one_hot_bad_sub_out)-numBadSubOutLeft+p])
			#print loopInd
			#loopInd += 1
		#print numpy.array(batchArr).shape
		#print len(batchArr)
		#print "dhvani"
		b = numpy.array(batchArr)
		#print b.shape
		yield b


def getInputTestTen():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, passInsErrorInd = perform(2037)
	fileInd = 2037
	batchInd = 1

	if True:
		if True:	
			#print passInsErrorInd
			print "ERROR IND"
			print one_hot_good
			toPassOne = []
			for x in range(10):
				y = x
				if y < len(one_hot_good):
					toPassOne.append(one_hot_good[y])
			toPassTwo = []	
			for x in range(10):
			
				y = passInsErrorInd - x
				if y < len(one_hot_bad_ins):
					toPassTwo.append(one_hot_bad_ins[y])
			toPassThree = []	
			for x in range(10):
				y = x
				if y < len(one_hot_bad_del):				
					toPassThree.append(one_hot_bad_del[y])
			toPassFour = []
			for x in range(10):
				y = x
				if y < len(one_hot_bad_sub):	
					toPassFour.append(one_hot_bad_sub[y])
			
			#print len(toPass)
			#print len(toPassOne)
			#print len(toPassTwo)
			#print len(toPassThree)
			#print len(toPassFour)
			#toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			toPass = toPassTwo[:]
			a = numpy.array(toPass).astype(int)
			#print b.shape
			return a
			#print numpy.array(toPass).shape
			#print "mine too"
			batchInd += 1
			windowInd += 1
		else:
			#print "NEXT FILE"
		
			old_one_hot_good = one_hot_good[:]
			old_one_hot_bad_ins = one_hot_bad_ins[:]
			old_one_hot_bad_del = one_hot_bad_del[:]
			old_one_hot_bad_sub = one_hot_bad_sub[:]

			numGoodLeft = len(one_hot_good) % 10
			numBadInsLeft = len(one_hot_bad_ins) % 10
			numBadDelLeft = len(one_hot_bad_del) % 10
			numBadSubLeft = len(one_hot_bad_sub) % 10

			fileInd += 1
			windowInd = 0
			one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _ = perform(fileInd)
			while(one_hot_good == None):
				fileInd+=1
				one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _ = perform(fileInd)
	
			
			for p in range(numGoodLeft):
				one_hot_good.insert(p, old_one_hot_good[len(old_one_hot_good)-numGoodLeft+p])
			for p in range(numBadInsLeft):
				one_hot_bad_ins.insert(p, old_one_hot_bad_ins[len(old_one_hot_bad_ins)-numBadInsLeft+p])
			for p in range(numBadDelLeft):
				one_hot_bad_del.insert(p, old_one_hot_bad_del[len(old_one_hot_bad_del)-numBadDelLeft+p])
			for p in range(numBadSubLeft):
				one_hot_bad_sub.insert(p, old_one_hot_bad_sub[len(old_one_hot_bad_sub)-numBadSubLeft+p])

def getOutputTestTen():
	_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(10)
	windowInd = 0
	fileInd = 10
	batchInd = 1
	while fileInd <= 11: # 462540
	#while windowInd < int(len(insArr)/10):
		sizes = [len(one_hot_good_out), len(one_hot_bad_ins_out),len(one_hot_bad_del_out),len(one_hot_bad_sub_out)]
		minSize = min(float(siz) for siz in sizes) # min of a generator
		if windowInd < int(minSize/10):		
			toPassOne = []
			for x in range(10):
				y = x + windowInd
				if y < len(one_hot_good_out):
					toPassOne.append(one_hot_good_out[y])
			toPassTwo = []	
			for x in range(10):
				y = x + windowInd
				if y < len(one_hot_bad_ins_out):
					toPassTwo.append(one_hot_bad_ins_out[y])
			toPassThree = []	
			for x in range(10):
				y = x + windowInd
				if y < len(one_hot_bad_del_out):
					toPassThree.append(one_hot_bad_del_out[y])
			toPassFour = []
			for x in range(10):
				y = x + windowInd
				if y < len(one_hot_bad_sub_out):
					toPassFour.append(one_hot_bad_sub_out[y])
			#print len(toPass)
			#toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			toPass = []
			if(batchInd == 1):
				toPass = toPassOne[:]
			elif(batchInd == 2):
				toPass = toPassTwo[:]
			elif(batchInd == 3):
				toPass = toPassThree[:]
			elif(batchInd == 4):
				toPass = toPassFour[:]
			if(batchInd % 4 == 0):
				batchInd = 1
			a = numpy.array(toPass).astype(int)
			#print b.shape
			yield a
			#print numpy.array(toPass).shape
			#print "mine"
			batchInd += 1
			windowInd += 1
		else:
			#print "NEXT FILE"

			old_one_hot_good_out = one_hot_good_out[:]
			old_one_hot_bad_ins_out = one_hot_bad_ins_out[:]
			old_one_hot_bad_del_out = one_hot_bad_del_out[:]
			old_one_hot_bad_sub_out = one_hot_bad_sub_out[:]

			numGoodOutLeft = len(one_hot_good_out) % 10
			numBadInsOutLeft = len(one_hot_bad_ins_out) % 10
			numBadDelOutLeft = len(one_hot_bad_del_out) % 10
			numBadSubOutLeft = len(one_hot_bad_sub_out) % 10

			fileInd += 1
			windowInd = 0
			_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(fileInd)
			while(one_hot_good_out == None):
				fileInd+=1
				_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(fileInd)

			for p in range(numGoodOutLeft):
				one_hot_good_out.insert(p, old_one_hot_good_out[len(old_one_hot_good_out)-numGoodOutLeft+p])
			for p in range(numBadInsOutLeft):
				one_hot_bad_ins_out.insert(p, old_one_hot_bad_ins_out[len(old_one_hot_bad_ins_out)-numBadInsOutLeft+p])
			for p in range(numBadDelOutLeft):
				one_hot_bad_del_out.insert(p, old_one_hot_bad_del_out[len(old_one_hot_bad_del_out)-numBadDelOutLeft+p])
			for p in range(numBadSubOutLeft):
				one_hot_bad_sub_out.insert(p, old_one_hot_bad_sub_out[len(old_one_hot_bad_sub_out)-numBadSubOutLeft+p])


@property
def log_path(self):
	return self.base_dir / "{self.name}.csv"

@property
def weight_path_pattern(self):
	return self.base_dir / (
            self.name + '-{epoch:02d}-{val_loss:.4f}.hdf5'
        )

# TODO: Make the alone integers constants
def initData():
	print "Start..."

	#main_input = Input(shape=(10,87), dtype='int32', name='main_input')
	allTrainData = cPickle.load( open( "train_pre_data.txt", "rb" ) )
	allValData = cPickle.load( open( "val_pre_data.txt", "rb" ) )
	print "GOT DATA"

	# Other Purposes
	sumOne = 0
	sumTwo = 0
	fileInd = 0
	for x in allTrainData:
		if x != -1:
			sumOne += len(x[1])
		fileInd += 1
	for y in allValData:
		if y != -1:
			sumTwo += len(y[1])
	print sumOne
	print sumTwo
	print "SUM"


	model = Sequential()
	model.add(Dense(4, activation='relu', input_shape=(10, 88), batch_size=66))
	model.add(Dropout(0.5))
	model.add(Flatten())
	model.add(Dense(4, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Activation('softmax'))

	# For a binary classification problem
	#model.compile(optimizer='rmsprop',
        #      loss='binary_crossentropy',
        #      metrics=['accuracy'])

	#opt = optimizers.SGD(lr=0.001, momentum=0.5)
	#opt = optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=1e-08, decay=0.0)
	opt = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.5)
	model.compile(loss = "categorical_crossentropy", optimizer = opt, metrics=['accuracy'])
	
	# NOT USING:
	#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

	#zipped = iter()
	#print type(zipped)
	
	'''
	testIn = getInputTen()
	testOut = getOutputValTen()
	s = 0
	for x in testIn:
		print x.shape
		print type(radha)
	print "Done"
	sys.exit()
	'''

	# FIRST THOUSAND TOKENS: 1090392
	# FIRST THOUSAND TOKENS:  948676 ( / 31 )
	# SECOnD THOUSAND TOKENS: 1353925

	# TRAIN: 1171580
	# VAL: 1462613

	# Train: 994
	# Val: 999

	history = model.fit_generator(
               	izip(getInputTen(allTrainData), getOutputTen(allTrainData)),
                steps_per_epoch=42600, #Before: 42 500
		validation_data=izip(getInputValTen(allValData), getOutputValTen(allValData)),
		validation_steps=53300, #Before: 53 300
                epochs=3000,  
		callbacks=[
                    ModelCheckpoint(
                        str(self.weight_path_pattern),
                        save_best_only=False,
                        save_weights_only=False,
                        mode='auto'
                    ),
                    CSVLogger(str(self.log_path), append=True),
                    EarlyStopping(patience=3, mode='auto')
                ]
                verbose=1	
            )

	'''
	 callbacks=[
                    ModelCheckpoint(
                        str(self.weight_path_pattern),
                        save_best_only=False,
                        save_weights_only=False,
                        mode='auto'
                    ),
                    CSVLogger(str(self.log_path), append=True),
                    EarlyStopping(patience=3, mode='auto')
                ]
	'''


	# list all data in history
	print(history.history.keys())
	print len(history.history.keys())
	
	
	
	# summarize history for accuracy
	
	plt.plot(history.history['acc'])
	plt.plot(history.history['val_acc'])
	plt.title('model accuracy')
	plt.ylabel('accuracy')
	plt.xlabel('epoch')
	plt.legend(['train', 'test'], loc='upper left')
	plt.show()
	# summarize history for loss
	plt.plot(history.history['loss'])
	plt.plot(history.history['val_loss'])
	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'test'], loc='upper left')
	plt.show()
	
	

	print "MODEL FIT"	

	print "SAVING"
	
	# serialize model to YAML
	model_yaml = model.to_yaml()
	with open("model_l.yaml", "w") as yaml_file:
		yaml_file.write(model_yaml)
	# serialize weights to HDF5
	model.save_weights("model_l.h5")
	print("Saved model to disk")
	print history.history['acc']
	print history.history['val_acc']
	print history.history['loss']
	print history.history['val_loss']
	
	sys.exit()
	#scores = model.evaluate_generator(izip(getInputTestTen(), getOutputTestTen()), steps=10)
	genIn = getInputTestTen()
	print type(genIn)
	print len(genIn)
	print genIn[0]
	
	input_testT = []
	for x in genIn:
		input_testT.append(x)

	print len(input_testT)
	print len(input_testT[0])
	print input_testT[0][0]
	from numpy import zeros, newaxis
	a = numpy.array(input_testT)
	print a.shape

	#outPredict = model.predict_generator(getInputTestTen(), steps=10, verbose=1)	
	outPredict = model.predict(genIn, batch_size=15, verbose=1)

	print "PREDICT"
	print len(outPredict)
	print outPredict.shape
	print len(outPredict[0])
	print outPredict[0]
	rounded = np.around(outPredict[0])
	print rounded
	#rounded = outPredict[0]
	#temp = rounded[:]
	#for x in temp:
	#a = numpy.array(rounded).astype(int)
	sums = []
	inds = []
	sum = 0.0
	radInd = 0
	for x in outPredict:
		print x
		sum = 0.0
		for y in x:
			sum = sum + y
		sums.append(sum)


	
	for x in range(9):
		inds.append(list(outPredict[x]).index(max(outPredict[x])))
	print max(outPredict[0])
	print list(outPredict[0]).index(max(outPredict[0]))
	print "MAX"
	for b in inds:
		print b

	print "SUM"
	for x in sums:
		print x

	sys.exit()		
	#outPredict = outPredict.astype(int)
	ind = 0
	for x in outPredict:
		rounded.append([round(x[ind]) for x in outPredict])
		ind += 1
	print rounded

	#scores = model.evaluate(a, c, batch_size=10)
	print "SCORE"
	cvscores = []
	print scores
	print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
	cvscores.append(scores[1] * 100)
	print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))
	
	print "TERMINATED"
	
if __name__ == '__main__':
	initData()
