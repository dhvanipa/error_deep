# Copyright 2017 Dhvani Patel

from __future__ import division

import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import javalang
from javac_parser import Java
import cStringIO
import codecs	

def tokenize(get):
	get = '\'\''
	print get
	tokGen = javalang.tokenizer.tokenize(get + ' ')
	for tok in tokGen:
		print tok

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def create_plot_fix(file_name):
	java = Java()
			

	with open(file_name, 'r') as csvfile:
   		check_reader = csv.reader(csvfile, delimiter=',')
		check_actual_reader = UnicodeReader(csvfile)		
		count = 1
		print "start"
		all_tokens = []
		#gen = utf_8_encoder(check_reader)

		for row in check_actual_reader:
			
			print row
			#print type(radha)
			print count
			toCompTok = row[9]
			getToks = java.lex(toCompTok)
			for token in getToks:
				vocabToCheck = token[0]	.encode()
				#print vocabToCheck
				if vocabToCheck not in all_tokens:
					all_tokens.append(vocabToCheck)
			count += 1
			
	print all_tokens
		

if __name__ == '__main__':
	file_name = sys.argv[1]
	#tokenize(file_name)
	create_plot_fix(file_name)
