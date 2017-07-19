# Copyright 2017 Dhvani Patel

from keras.models import Sequential
from keras.layers import Dense, Dropout, Input, Embedding, LSTM
from keras.models import Model
from keras import optimizers
from keras.callbacks import ModelCheckpoint, CSVLogger, EarlyStopping

import numpy
from Token import Token
from py_mutations_hub import perform
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from itertools import izip_longest
from itertools import izip

import matplotlib.pyplot as plt

# BATCH = 60
# So 15 of 4 of one window
# One 4:
# [Good, Insert, Delete, Sub]
WINDOW_SIZE = 10

# DEFINED:

# FIXED INPUT BITS = 87 (ONE TOKEN)
# FIXED OUTPUT BITS = 102 (2+2+3+10+85)
# WINDOW = 10, SO BATCH = 40 INPUT, 40 OUTPUT


def getInputTen():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _ = perform(0)
	windowInd = 0
	fileInd = 0
	batchInd = 1
	count = 0
	while fileInd <= 1000: # 462540
	#while windowInd < int(len(insArr)/10):
		sizes = [len(one_hot_good), len(one_hot_bad_ins),len(one_hot_bad_del),len(one_hot_bad_sub)]
		minSize = min(float(siz) for siz in sizes) # min of a generator
		print "file"
		print fileInd
		print minSize
		print windowInd
		print int((int(minSize) / 10))
		while windowInd < int((int(minSize) / 10)):
			print windowInd
			print "WINDOW"	
			batchInd = 1
			print len(one_hot_good)
			print len(one_hot_bad_ins)
			print len(one_hot_bad_del)
			print len(one_hot_bad_sub)	
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
			#print len(toPass)
			print len(toPassOne)
			print len(toPassTwo)
			print len(toPassThree)
			print len(toPassFour)
			#toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			#toPass = []
			
			while(batchInd % 5 != 0):
				toPass = []
				print "BATCH IND"
				print batchInd
				if(batchInd == 1):
					toPass = toPassOne[:]
				elif(batchInd == 2):
					toPass = toPassTwo[:]
				elif(batchInd == 3):
					toPass = toPassThree[:]
				elif(batchInd == 4):
					toPass = toPassFour[:]
				a = numpy.array(toPass).astype(int)
				print a.shape
				count+=1
				print "COUNT"
				print count
				#print b.shape
				yield a
				batchInd += 1
			#print numpy.array(toPass).shape
			print "mine too"
			windowInd += 1
		#else:
		print "NEXT FILE"
		print "DONE BRO"
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

def getOutputTen():
	_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(0)
	windowInd = 0
	fileInd = 0
	batchInd = 1
	while fileInd <= 1000: # 462540
	#while windowInd < int(len(insArr)/10):
		sizes = [len(one_hot_good_out), len(one_hot_bad_ins_out),len(one_hot_bad_del_out),len(one_hot_bad_sub_out)]
		minSize = min(float(siz) for siz in sizes) # min of a generator
		while windowInd < int((int(minSize)/10)):	
			batchInd = 1	
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
			while(batchInd % 5 != 0):
				toPass = []
				print "BATCH IND"
				print batchInd
				if(batchInd == 1):
					toPass = toPassOne[:]
				elif(batchInd == 2):
					toPass = toPassTwo[:]
				elif(batchInd == 3):
					toPass = toPassThree[:]
				elif(batchInd == 4):
					toPass = toPassFour[:]
				a = numpy.array(toPass).astype(int)
				print a.shape
				#count+=1
				#print "COUNT"
				#print count
				#print b.shape
				yield a
				batchInd += 1
			windowInd += 1

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


def getInputValTen():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _ = perform(1001)
	windowInd = 0
	fileInd = 1001
	batchInd = 1
	count = 0
	while fileInd <= 2000: # 462540
	#while windowInd < int(len(insArr)/10):
		sizes = [len(one_hot_good), len(one_hot_bad_ins),len(one_hot_bad_del),len(one_hot_bad_sub)]
		minSize = min(float(siz) for siz in sizes) # min of a generator
		print "file"
		print fileInd
		print minSize
		print windowInd
		print int((int(minSize) / 10))
		while windowInd < int((int(minSize) / 10)):
			print windowInd
			print "WINDOW"	
			batchInd = 1
			print len(one_hot_good)
			print len(one_hot_bad_ins)
			print len(one_hot_bad_del)
			print len(one_hot_bad_sub)	
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
			#print len(toPass)
			print len(toPassOne)
			print len(toPassTwo)
			print len(toPassThree)
			print len(toPassFour)
			#toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			#toPass = []
			
			while(batchInd % 5 != 0):
				toPass = []
				print "BATCH IND"
				print batchInd
				if(batchInd == 1):
					toPass = toPassOne[:]
				elif(batchInd == 2):
					toPass = toPassTwo[:]
				elif(batchInd == 3):
					toPass = toPassThree[:]
				elif(batchInd == 4):
					toPass = toPassFour[:]
				a = numpy.array(toPass).astype(int)
				print a.shape
				count+=1
				print "COUNT"
				print count
				#print b.shape
				yield a
				batchInd += 1
			#print numpy.array(toPass).shape
			print "mine too"
			windowInd += 1
		#else:
		print "NEXT FILE"
		print "DONE BRO"
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

def getOutputValTen():
	_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(1001)
	windowInd = 0
	fileInd = 1001
	batchInd = 1
	while fileInd <= 2000: # 462540
	#while windowInd < int(len(insArr)/10):
		sizes = [len(one_hot_good_out), len(one_hot_bad_ins_out),len(one_hot_bad_del_out),len(one_hot_bad_sub_out)]
		minSize = min(float(siz) for siz in sizes) # min of a generator
		while windowInd < int((int(minSize)/10)):	
			batchInd = 1	
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
			while(batchInd % 5 != 0):
				toPass = []
				print "BATCH IND"
				print batchInd
				if(batchInd == 1):
					toPass = toPassOne[:]
				elif(batchInd == 2):
					toPass = toPassTwo[:]
				elif(batchInd == 3):
					toPass = toPassThree[:]
				elif(batchInd == 4):
					toPass = toPassFour[:]
				a = numpy.array(toPass).astype(int)
				print a.shape
				#count+=1
				#print "COUNT"
				#print count
				#print b.shape
				yield a
				batchInd += 1
			windowInd += 1

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

def getInputTestTen():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _ = perform(2)
	windowInd = 0
	fileInd = 2
	batchInd = 1
	#while fileInd <= 2: # 462540
	if True:
	#while windowInd < int(len(insArr)/10):
		sizes = [len(one_hot_good), len(one_hot_bad_ins),len(one_hot_bad_del),len(one_hot_bad_sub)]
		minSize = min(float(siz) for siz in sizes) # min of a generator
		print "file"
		print fileInd
		if windowInd < int((minSize / 10)):	
			print len(one_hot_good)
			print len(one_hot_bad_ins)
			print len(one_hot_bad_del)
			print len(one_hot_bad_sub)	
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
			#print len(toPass)
			print len(toPassOne)
			print len(toPassTwo)
			print len(toPassThree)
			print len(toPassFour)
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


	model = Sequential()
	model.add(Dense(102, activation='relu', input_shape=(88,)))
	model.add(Dropout(0.5))
	model.add(Dense(102, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(102, activation='softmax'))
	

	# For a binary classification problem
	#model.compile(optimizer='rmsprop',
        #      loss='binary_crossentropy',
        #      metrics=['accuracy'])

	opt = optimizers.SGD(lr=0.001)
	#opt = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
	model.compile(loss = "categorical_crossentropy", optimizer = opt, metrics=['accuracy'])

	#zipped = iter()
	#print type(zipped)

	history = model.fit_generator(
               	izip(getInputTen(), getOutputTen()),
                steps_per_epoch=12,
		validation_data=izip(getInputValTen(), getOutputValTen()),
		validation_steps=12,
                epochs=200,   
                verbose=2	
            )
	'''
	callbacks=[
                    ModelCheckpoint(
                        str(weight_path_pattern),
                        save_best_only=False,
                        save_weights_only=False,
                        mode='auto'
                    ),
                    CSVLogger(str(log_path), append=True),
                    EarlyStopping(patience=3, mode='auto')
                ],  
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
	
	        
	#scores = model.evaluate_generator(izip(getInputTestTen(), getOutputTestTen()), steps=10)
	genIn = getInputTestTen()
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
	outPredict = model.predict(a, batch_size=4, verbose=1)

	print "PREDICT"
	print len(outPredict)
	print outPredict.shape
	#outPredict = outPredict.astype(int)
	for x in outPredict:
		print x[0]

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
