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
# WINDOW SIZE = 10

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


def create_batches():
	one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub = perform()
	print "Finished..."
	
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
	
	# feedData(train_input	

	#return train_input, train_output

def initData():
	print "Start..."
	create_batches()
	model = Sequential()
	# Fit the model
	#model.fit(iter(train_input), iter(train_output), epochs=150, batch_size=10)
	#train_input, train_output = create_batches()


if __name__ == '__main__':
	initData()
