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
	opt = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.9)
	loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

	genIn = getInputTestTen()
	outPredict = loaded_model.predict(genIn, batch_size=15, verbose=1)

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

	#score = loaded_model.evaluate(X, Y, verbose=0)
	#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


if __name__ == '__main__':
	predictData()
