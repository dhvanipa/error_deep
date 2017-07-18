# Copyright 2017 Dhvani Patel

from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy
from Token import Token
from py_mutations_hub import perform
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from itertools import izip_longest
from itertools import izip
from keras import optimizers


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
	while fileInd <= 10: # 462540
	#while windowInd < int(len(insArr)/10):
		if windowInd < int(len(one_hot_bad_ins)/10):		
			toPassOne = []
			for x in range(10):
				y = x + windowInd
				toPassOne.append(one_hot_good[y])
			toPassTwo = []	
			for x in range(10):
				y = x + windowInd
				toPassTwo.append(one_hot_bad_ins[y])
			toPassThree = []	
			for x in range(10):
				y = x + windowInd
				toPassThree.append(one_hot_bad_del[y])
			toPassFour = []
			for x in range(10):
				y = x + windowInd
				toPassFour.append(one_hot_bad_sub[y])
			#print len(toPass)
			toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			a = numpy.array(toPass)
			#print b.shape
			yield a
			#print numpy.array(toPass).shape
			#print "mine too"
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

def getOutputTen():
	_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(0)
	windowInd = 0
	fileInd = 0
	while fileInd <= 10: # 462540
	#while windowInd < int(len(insArr)/10):
		if windowInd < int(len(one_hot_bad_ins_out)/10):		
			toPassOne = []
			for x in range(10):
				y = x + windowInd
				toPassOne.append(one_hot_good_out[y])
			toPassTwo = []	
			for x in range(10):
				y = x + windowInd
				toPassTwo.append(one_hot_bad_ins_out[y])
			toPassThree = []	
			for x in range(10):
				y = x + windowInd
				toPassThree.append(one_hot_bad_del_out[y])
			toPassFour = []
			for x in range(10):
				y = x + windowInd
				toPassFour.append(one_hot_bad_sub_out[y])
			#print len(toPass)
			toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			a = numpy.array(toPass)
			#print b.shape
			yield a
			#print numpy.array(toPass).shape
			#print "mine"
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


def getInputValTen():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _ = perform(11)
	windowInd = 0
	fileInd = 11
	while fileInd <= 20: # 462540
	#while windowInd < int(len(insArr)/10):
		if windowInd < int(len(one_hot_bad_ins)/10):		
			toPassOne = []
			for x in range(10):
				y = x + windowInd
				toPassOne.append(one_hot_good[y])
			toPassTwo = []	
			for x in range(10):
				y = x + windowInd
				toPassTwo.append(one_hot_bad_ins[y])
			toPassThree = []	
			for x in range(10):
				y = x + windowInd
				toPassThree.append(one_hot_bad_del[y])
			toPassFour = []
			for x in range(10):
				y = x + windowInd
				toPassFour.append(one_hot_bad_sub[y])
			#print len(toPass)
			toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			a = numpy.array(toPass)
			#print b.shape
			yield a
			#print numpy.array(toPass).shape
			#print "mine too"
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

def getOutputValTen():
	_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(11)
	windowInd = 0
	fileInd = 11
	while fileInd <= 20: # 462540
	#while windowInd < int(len(insArr)/10):
		if windowInd < int(len(one_hot_bad_ins_out)/10):		
			toPassOne = []
			for x in range(10):
				y = x + windowInd
				toPassOne.append(one_hot_good_out[y])
			toPassTwo = []	
			for x in range(10):
				y = x + windowInd
				toPassTwo.append(one_hot_bad_ins_out[y])
			toPassThree = []	
			for x in range(10):
				y = x + windowInd
				toPassThree.append(one_hot_bad_del_out[y])
			toPassFour = []
			for x in range(10):
				y = x + windowInd
				toPassFour.append(one_hot_bad_sub_out[y])
			#print len(toPass)
			toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			a = numpy.array(toPass)
			#print b.shape
			yield a
			#print numpy.array(toPass).shape
			#print "mine"
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

def getInputTestTen():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _ = perform(0)
	windowInd = 0
	fileInd = 0
	while fileInd <= 10: # 462540
	#while windowInd < int(len(insArr)/10):
		if windowInd < int(len(one_hot_bad_ins)/10):		
			toPassOne = []
			for x in range(10):
				y = x + windowInd
				toPassOne.append(one_hot_good[y])
			toPassTwo = []	
			for x in range(10):
				y = x + windowInd
				toPassTwo.append(one_hot_bad_ins[y])
			toPassThree = []	
			for x in range(10):
				y = x + windowInd
				toPassThree.append(one_hot_bad_del[y])
			toPassFour = []
			for x in range(10):
				y = x + windowInd
				toPassFour.append(one_hot_bad_sub[y])
			#print len(toPass)
			toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			a = numpy.array(toPass)
			#print b.shape
			yield a
			#print numpy.array(toPass).shape
			#print "mine too"
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
	_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(0)
	windowInd = 0
	fileInd = 0
	while fileInd <= 10: # 462540
	#while windowInd < int(len(insArr)/10):
		if windowInd < int(len(one_hot_bad_ins_out)/10):		
			toPassOne = []
			for x in range(10):
				y = x + windowInd
				toPassOne.append(one_hot_good_out[y])
			toPassTwo = []	
			for x in range(10):
				y = x + windowInd
				toPassTwo.append(one_hot_bad_ins_out[y])
			toPassThree = []	
			for x in range(10):
				y = x + windowInd
				toPassThree.append(one_hot_bad_del_out[y])
			toPassFour = []
			for x in range(10):
				y = x + windowInd
				toPassFour.append(one_hot_bad_sub_out[y])
			#print len(toPass)
			toPass = np.array((toPassOne, toPassTwo, toPassThree, toPassFour))
			#print toPass.shape
			a = numpy.array(toPass)
			#print b.shape
			yield a
			#print numpy.array(toPass).shape
			#print "mine"
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

# TODO: Make the alone integers constants
def initData():
	print "Start..."
	
	model = Sequential()
	model.add(Dense(102, activation='relu', input_shape=(10,87)))
	model.add(Dropout(0.5))
	model.add(Dense(102, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(102, activation='softmax'))
	

	# For a binary classification problem
	#model.compile(optimizer='rmsprop',
        #      loss='binary_crossentropy',
        #      metrics=['accuracy'])

	opt = optimizers.SGD(lr=0.3)
	model.compile(loss = "categorical_crossentropy", optimizer = opt)

	#zipped = iter()
	#print type(zipped)

	model.fit_generator(
               	izip(getInputTen(), getOutputTen()),
                steps_per_epoch=5,
		validation_data=izip(getInputValTen(), getOutputValTen()),
		validation_steps=15,
                epochs=10,      
                verbose=3,	
            )
	
	
	x_test = []
	steps = 0
	g = getInputTestTen()
	for t in g:
		if steps > 5: 
			break
		steps += 1	
		#print type(t)	
		x_test = t

	y_test = []
	steps = 0
	for t in getOutputTestTen():
		if steps > 5: 
			break	
		steps += 1			
		y_test = t

	print "MODEL FIT"	
	print len(x_test)
	print x_test[0][0]
	print len(y_test)
	
	a = numpy.array(x_test)
	n = numpy
	print a.shape
	#b = a[None, :, :]

	c = numpy.array(y_test)
	print c.shape
	#d = c[None, :, :]
	
	scores = model.evaluate(a, c, batch_size=10)
	print "SCORE"
	#cvscores = []
	print scores
	#print("%s: %.2f%%" % (model.metrics_names, scores*100))
	#cvscores.append(scores * 100)
	#print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))
	
	print "TERMINATED"
	
if __name__ == '__main__':
	initData()
