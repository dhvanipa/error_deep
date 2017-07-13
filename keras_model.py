# Copyright 2017 Dhvani Patel

from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy
from Token import Token
from py_mutations_hub import perform

# BATCH = 60
# So 15 of 4 of one window
# One 4:
# [Good, Insert, Delete, Sub]
# WINDOW SIZE = 10

def create_batches():
	# Copyright 2016, 2017 Eddie Antonio Santos <easantos@ualberta.ca>
        """
        Return a tuple of infinite training and validation examples,
        respectively.
        """
        training = LoopBatchesEndlessly(
            filehashes=self.training_set,
            vectors_path=self.vectors_path,
            batch_size=self.batch_size,
            context_length=self.context_length,
            backwards=self.backwards
        )
        validation = LoopBatchesEndlessly(
            filehashes=self.validation_set,
            vectors_path=self.vectors_path,
            batch_size=self.batch_size,
            context_length=self.context_length,
            backwards=self.backwards
        )
        return training, validation

def initData():
	print "Start..."
	one_hot_all = perform()
	print len(one_hot_all)

	train_input, train_output = create_batches()


if __name__ == '__main__':
	initData()
