# Copyright 2017 Dhvani Patel

from keras.models import Sequential
from keras.layers import Dense, Dropout, Input, Embedding, LSTM
from keras.models import Model
from keras import optimizers
from keras.callbacks import ModelCheckpoint, CSVLogger, EarlyStopping
from keras.models import model_from_yaml

from Token import Token
from py_mutations_hub import perform
import numpy

import os

def getInputTestDat():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(2001)
	while(one_hot_good == 1):
			one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, _ = perform(2001)
	#print type(one_hot_good)
	#print one_hot_good
	windowInd = 0
	fileInd = 2001
	batchInd = 1
	#count = 0
	while fileInd <= 2500: # 462540
	#while windowInd < int(len(insArr)/10):
		sizes = [len(one_hot_good), len(one_hot_bad_ins),len(one_hot_bad_del),len(one_hot_bad_sub)]
		minSize = min(float(siz) for siz in sizes) # min of a generator
		#print "file"
		#print fileInd
		#print minSize
		#print windowInd
		#print int((int(minSize) / 10))
		while windowInd < int((int(minSize) / 10)):
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
			print "RADHA"
			while(batchInd % 4 != 0):
				toPass = []
				#print "BATCH IND"
				#print batchInd
				if(batchInd == 1):
					toPass = toPassOne[:]
					print "BATCH IND"
				elif(batchInd == 2):
					toPass = toPassTwo[:]
					print "BATCH IND T"
				elif(batchInd == 3):
					toPass = toPassThree[:]
					print "BATCH IND TT"
				elif(batchInd == 4):
					print "here"
					toPass = toPassTwo[:]
				a = numpy.array(toPass).astype(int)
				#print a.shape
				#count+=1
				#print "COUNT"
				#print count
				#print b.shape
				print len(a)
				yield a
				batchInd += 1
			
			#print numpy.array(toPass).shape
			#print "mine too"
			#a = numpy.array(toPass)
			#print a.shape
			#yield a
			windowInd += 1
		#else:
		#print "NEXT FILE"
		#print "DONE BRO"
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

def getInputTestTen():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _, passInsErrorInd = perform(2037)
	fileInd = 2037
	batchInd = 1

	if True:
		if True:	
			#print passInsErrorInd
			print "ERROR IND"
			#print one_hot_good
			print len(one_hot_bad_del)
			print len(one_hot_good)
			print len(one_hot_bad_ins)
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
			print len(toPassOne)
			print len(toPassTwo)
			print len(toPassThree)
			#print len(toPassFour)
			#toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			toPass = toPassTwo[:]
			a = numpy.array(toPass).astype(int)
			print a.shape
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

def predictData():
	# load YAML and create model
	yaml_file = open('model_l.yaml', 'r')
	loaded_model_yaml = yaml_file.read()
	yaml_file.close()
	loaded_model = model_from_yaml(loaded_model_yaml)
	# load weights into new model
	loaded_model.load_weights("model_l.h5")
	print("Loaded model from disk")
 
	# evaluate loaded model on test data
	opt = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.5)
	loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

	#genIn = getInputTestTen()
	#outPredict = loaded_model.predict(genIn, batch_size=15, verbose=1)

	# 1000 -> 10 000
	# 100 -> 1000
	# 300 -> 3000
	# TIMES 10
	#genIn = getInputTestDat()
	#for x in genIn:
	#	print x
	#	sys.exit()
	outPredict = loaded_model.predict_generator(getInputTestDat(), 9000, 3, verbose=1)

	print "PREDICT"
	print outPredict
	sums = []
	inds = []
	sum = 0.0
	radInd = 0
	for x in outPredict:
		#print x
		sum = 0.0
		for y in x:
			sum = sum + y
		sums.append(sum)

	for x in range(len(list(outPredict))):
		inds.append(list(outPredict[x]).index(max(outPredict[x])))
	print max(outPredict[0])
	print list(outPredict[0]).index(max(outPredict[0]))
	print "MAX"
        countGood = -1
        countIns = -1
	countDel = -1
	iterInd = 0
	for b in inds:
		if iterInd == 3:
			iterInd = 0
		
		if iterInd == 0:
               		if b == 0:
				countGood += 1
		if iterInd == 1: 		
			if b == 3:
				countIns += 1
		if iterInd == 2:
			if b == 2:
				countDel += 1
		iterInd += 1
		print b
        print len(inds)
	print countGood
	print countIns
	print countDel

	#print "SUM"
	#for x in sums:
	#	print x

	#score = loaded_model.evaluate(X, Y, verbose=0)
	#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


if __name__ == '__main__':
	predictData()
