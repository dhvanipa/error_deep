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

# BATCH = 60
# So 15 of 4 of one window
# One 4:
# [Good, Insert, Delete, Sub]
WINDOW_SIZE = 10

# DEFINED:

# FIXED INPUT BITS = 87 (ONE TOKEN)
# FIXED OUTPUT BITS = 102 (2+2+3+10+85)
# WINDOW = 10, SO BATCH = 40 INPUT, 40 OUTPUT


def getGoodTen():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub, _, _, _, _ = perform(2)
	windowInd = 0
	fileInd = 2
	while fileInd <= 2: # 462540
	#while windowInd < int(len(insArr)/10):
		if windowInd < int(len(one_hot_bad_ins)/10):		
			toPass = []
			for x in range(10):
				y = x + windowInd
				toPass.append(one_hot_good[y])	
			for x in range(10):
				y = x + windowInd
				toPass.append(one_hot_bad_ins[y])
			for x in range(10):
				y = x + windowInd
				toPass.append(one_hot_bad_del[y])
			for x in range(10):
				y = x + windowInd
				toPass.append(one_hot_bad_sub[y])
			#print len(toPass)
			yield toPass
			windowInd += 1
		else:
			print "NEXT FILE"
		
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
			
			for p in range(numGoodLeft):
				one_hot_good.insert(p, old_one_hot_good[len(old_one_hot_good)-numGoodLeft+p])
			for p in range(numBadInsLeft):
				one_hot_bad_ins.insert(p, old_one_hot_bad_ins[len(old_one_hot_bad_ins)-numBadInsLeft+p])
			for p in range(numBadDelLeft):
				one_hot_bad_del.insert(p, old_one_hot_bad_del[len(old_one_hot_bad_del)-numBadDelLeft+p])
			for p in range(numBadSubLeft):
				one_hot_bad_sub.insert(p, old_one_hot_bad_sub[len(old_one_hot_bad_sub)-numBadSubLeft+p])

def getBadTen():
	_, _, _, _, one_hot_good_out, one_hot_bad_ins_out, one_hot_bad_del_out, one_hot_bad_sub_out = perform(2)
	windowInd = 0
	fileInd = 2
	while fileInd <= 2: # 462540
	#while windowInd < int(len(insArr)/10):
		if windowInd < int(len(one_hot_bad_ins_out)/10):		
			toPass = []
			for x in range(10):
				y = x + windowInd
				toPass.append(one_hot_good_out[y])	
			for x in range(10):
				y = x + windowInd
				toPass.append(one_hot_bad_ins_out[y])
			for x in range(10):
				y = x + windowInd
				toPass.append(one_hot_bad_del_out[y])
			for x in range(10):
				y = x + windowInd
				toPass.append(one_hot_bad_sub_out[y])
			#print len(toPass)
			yield toPass
			windowInd += 1
		else:
			print "NEXT FILE"

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

			for p in range(numGoodOutLeft):
				one_hot_good_out.insert(p, old_one_hot_good_out[len(old_one_hot_good_out)-numGoodOutLeft+p])
			for p in range(numBadInsOutLeft):
				one_hot_bad_ins_out.insert(p, old_one_hot_bad_ins_out[len(old_one_hot_bad_ins_out)-numBadInsOutLeft+p])
			for p in range(numBadDelOutLeft):
				one_hot_bad_del_out.insert(p, old_one_hot_bad_del_out[len(old_one_hot_bad_del_out)-numBadDelOutLeft+p])
			for p in range(numBadSubOutLeft):
				one_hot_bad_sub_out.insert(p, old_one_hot_bad_sub_out[len(old_one_hot_bad_sub_out)-numBadSubOutLeft+p])
			
'''
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

class feedData():

	def __init__(self, x_set, y_set, batch_size):
    		self.X,self.y = x_set,y_set
    		self.batch_size = batch_size

	def __len__(self):
    		return len(self.X) // self.batch_size

	def __getitem__(self,idx):
    		batch_x = self.X[idx*self.batch_size:(idx+1)*self.batch_size]
    		batch_y = self.y[idx*self.batch_size:(idx+1)*self.batch_size]
    		return np.array([batch_x]), np.array(batch_y)

'''
def create_batches():
	print "Creating batches..."
	
	
	
	inputTenG = []
	outputTenB = []
	for wow in firstTenGG:
		inputTenG.append(wow)
	for woh in firstTenBG:
		outputTenB.append(woh)

	
	print "Finished..."

	print len(inputTenG)
	print len(outputTenB)

	print "Constants"

	print len(inputTenG[0][0])
	print len(inputTenG[0])

	print len(outputTenB[0][0])
	print len(outputTenB[0])

	print "Terminate"


	'''
	ohg_g = chunker(one_hot_good, 10)
	ohbi_g = chunker(one_hot_bad_ins, 10)
	ohbd_g = chunker(one_hot_bad_del, 10)
	ohbs_g = chunker(one_hot_bad_sub, 10)
	
	ohg_group = []
	for rad in ohg_g:
		ohg_group.append(rad)

	ohbi_group = []
	for rad in ohbi_g:
		ohbi_group.append(rad)

	ohbd_group = []
	for rad in ohbd_g:
		ohbd_group.append(rad)

	ohbs_group = []
	for rad in ohbs_g:
		ohbs_group.append(rad)
			
	print len(ohg_group)
	print len(ohbi_group)
	print len(ohbd_group)
	#print ohbd_group[53]
	print len(ohbs_group)

	goodA = np.array(ohg_group)
	insA = np.array(ohbi_group)
	delA = np.array(ohbd_group)
	subA = np.array(ohbs_group)
			
	temp = np.insert(subA, np.arange(len(delA)), delA)
	temp2 = np.insert(temp, np.arange(len(insA)), insA)
	train_input = np.insert(temp2, np.arange(len(goodA)), goodA)
	'''
	# feedData(train_input	

	#return train_input, train_output

def initData():
	print "Start..."
	create_batches()
	model = Sequential()
	model.add(Dense(64, activation='relu', input_dim=20))
	model.add(Dropout(0.5))
	model.add(Dense(64, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(10, activation='softmax'))
	

	# For a binary classification problem
	model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

	firstTenGG = getGoodTen()
	firstTenBG = getBadTen()

	model.fit_generator(
               	 zip(firstTenGG, firstTenBG),
                steps_per_epoch=5,
                epochs=4,      
                verbose=1,	
            )
	#model.fit(iter(train_input), iter(train_output), epochs=150, batch_size=10)
	#train_input, train_output = create_batches()


if __name__ == '__main__':
	initData()
