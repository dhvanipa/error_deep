# Copyright 2017 Dhvani Patel

from __future__ import division

import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import javalang
from javac_parser import Java
import codecs
import cStringIO

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


def create_plot_fix(file_name):
	java = Java()
	ref_lines = []
	ref_col_lines = []
	with open("/home/dhvani/Documents/java_fixes_col.csv", 'r') as reffileCol:
			ref_reader_col = csv.reader(reffileCol, delimiter=',')
			for col in ref_reader_col:
				ref_col_lines.append(col)

	with open("/home/dhvani/java-mistakes-data/mistakes.csv", 'r') as reffile:
		ref_reader = csv.reader(reffile, delimiter=',')
		count = 0
		for line in ref_reader:
			#print line
			#print count
			for col in ref_col_lines:
					#print "here"
					#print col
					#print line[0]
					if col[0] == line[0] and col[1] == line[1]:
						ref_lines.append([line[0], line[1], line[4], col[3], col[5], line[6], line[5], line[8]])
			count +=1	
	#print len(ref_lines)
	del ref_lines[0]
	#print len(ref_lines)
	#sys.exit()
	vocab_javac = ["EQ", "EOF", "IDENTIFIER", "RPAREN", "SEMI", "RBRACE", "ELLIPSIS", "COLCOL", "INT", "PLUS", "CATCH", "STAR", "STRINGLITERAL", "INTERFACE", "VOLATILE", "PUBLIC", "ENUM", "LPAREN", "IMPORT", "ELSE", "IF", "INTLITERAL", "LBRACE", "COMMA", "DOT", "PLUSPLUS", "PERCENT", "FINAL", "WHILE", "SUPER", "GT", "COLON", "CLASS", "BANG", "CARET", "PRIVATE", "RBRACKET", "LT", "SLASH", "PACKAGE", "MONKEYS_AT", "FLOAT", "SUBSUB", "STATIC", "RETURN", "DOUBLELITERAL", "UNDERSCORE", "BYTE", "THROWS", "LBRACKET", "THIS", "EQEQ", "SUB", "CHAR", "NEW", "TRUE", "FLOATLITERAL", "FOR", "ARROW", "DOUBLE", "BANGEQ", "LTEQ", "CHARLITERAL", "DO", "EXTENDS", "QUES", "NULL", "STRICTFP", "AMP", "TRY", "AMPAMP", "PROTECTED", "THROW", "SWITCH", "CASE", "LONG", "INSTANCEOF", "ASSERT", "FALSE", "DEFAULT", "GTEQ"]
	actual_mapped = ["=", "EOF", "<IDENTIFIER>", ")", ";", "}", "...", "::", "<NUMBER>", "+", "catch", "*", "<STRING>", "interface", "volatile", "public", "enum", "(", "import", "else", "if", "<NUMBER>", "{", ",", ".", "++", "%", "final", "while", "super", ">", ":", "class", "!", "^", "private", "]", "<", "/", "package", "@", "float", "--", "static", "return", "<NUMBER>", "_", "byte", "throws", "[", "this", "==", "-", "char", "new", "true", "<NUMBER>", "for", "->", "double", "!=", "<=", "<STRING>", "do", "extends", "?", "null", "strictfp", "&", "try", "&&", "protected", "throw", "switch", "case", "long", "instanceof", "assert", "false", "default", ">="]


	with open(file_name, 'r') as csvfile:
   		check_reader = csv.reader(csvfile, delimiter=',')
		check_actual_reader = UnicodeReader(csvfile)	
		beforeS = -1
		beforeM = -1
		actual_tok = ''
		countRank = -1
		all_ranks = []
		flagIsDel = False
		print "start"
		fileNo = 0
		for row in check_actual_reader:
			fileNo += 1
			print fileNo
			#print row
			checkType = row[8]
			if checkType == 'd':
				flagIsDel = True
			else:
				flagIsDel = False
			
        		sfid = row[1]
			meid = row[2]
			#print row
			if sfid == beforeS and meid == beforeM:
				countRank += 1
				toCompTok = row[9]
				
				if toCompTok != '':
					print "----------------------------------"
					print toCompTok
					getToks = java.lex(toCompTok)
					print getToks
					#assert len(getToks) <= 3
					toCompTok = getToks
					
					print toCompTok
				
				for token in toCompTok:
					getInd = vocab_javac.index(token[0])
					actual_vToken = actual_mapped[getInd]
					if actual_vToken == actual_tok and row[5] == actual_line and row[8] == actual_class:
						all_ranks.append(countRank)
						actual_tok = ''

			else:
				if actual_tok != '':
					all_ranks.append(0)
				actual_tok = ''
				actual_line = -1
				actual_col_start = -1
				actual_col_end = -1
				actual_class = ''
				countRank = 1
				for line in ref_lines:
					if line[0] == sfid and line[1] == meid:
						# Files matched
						actual_line = line[2]
						actual_col_start = line[3]
						actual_col_end = line[4]
						actual_class = line[5]
						if flagIsDel == True:
							actual_tok = line[6]
						else:
							actual_tok = line[7]
						if actual_class == 'x':
							actual_class = 'd'
						#print actual_tok
						break
				#print count
				#assert actual_tok != ''
				beforeS = sfid
				beforeM = meid
				print "ROW"
				print row
				
				

				toCompTokD = row[9]
				print toCompTokD
				# TOKENIZE TOKEN:
				#print row
				
				if toCompTokD != '':
					print "----------------------------------"
					print toCompTokD
					getToks = java.lex(toCompTokD)
					print getToks
					#assert len(getToks) <= 3
					toCompTokD = getToks
					
					print toCompTokD
				#print type(radha)
				for token in toCompTokD:
					getInd = vocab_javac.index(token[0])
					actual_vToken = actual_mapped[getInd]
					'''
					print "GO"
					print actual_vToken
					print actual_tok
					print "---"
					print row[5]
					print actual_line
					print "---"
					print row[6]
					print actual_col_start
					print row[7]
					print actual_col_end
					print "---"
					print row[8]
					print actual_class
					print "STOP"
					'''
					# and row[6] >= actual_col_start and row[7] <= actual_col_end 
					if actual_vToken == actual_tok and row[5] == actual_line and row[8] == actual_class:
						all_ranks.append(countRank)
						actual_tok = ''
					#print type(radha)
			
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

		ax1.set_title('MRR For Eclipse: True Fix')
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
