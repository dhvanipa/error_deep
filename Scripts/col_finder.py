import csv
import os
from javac_parser import Java
from io import open
import sys
import keyword
import difflib

def getCol():
	rootdir = '/home/dhvani/java-mistakes-data'
	
	strPathsBef = []
	strPathsAft = []

	# Init java tokenizer:
	java = Java()

	for subdir, dirs, files in os.walk(rootdir):
    		for file in files:
			path = os.path.join(subdir, file)
			if "mistakes.csv" not in path:
				if "after.java" not in path:
					#print path
					strPathsBef.append(path)
				elif "after.java" in path:
					strPathsAft.append(path)
	# print strPaths
	assert len(strPathsBef) == len(strPathsAft)

	skip = 3530
	for loopInd in range(len(strPathsBef)):	
		#print loopInd
		if loopInd+skip == 2785:
			continue
		loopInd += skip	
		print loopInd
		beforeStrList = []
		afterStrList = []
		beforeF = strPathsBef[loopInd]
		afterF = strPathsAft[loopInd]
		#beforeF = "/home/dhvani/java-mistakes-data/10827021/387968016/before.java"
		#afterF = "/home/dhvani/java-mistakes-data/10827021/387968016/after.java"
		beforeToks = []
		with open(beforeF, 'r') as myfile:
    			dataBefore=myfile.read()
			beforeToks = java.lex(dataBefore)
			for token in beforeToks:
				if token[0] in ["DOUBLELITERAL", "FLOATLITERAL"]:
					beforeStrList.append("INTLITERAL")
				else:
					beforeStrList.append(token[0])
				#print token[1]
		#print "---------------------"
		afterToks = []
		with open(afterF, 'r') as myfile:
    			dataAfter=myfile.read()
			afterToks = java.lex(dataAfter)
			for token in afterToks:
				if token[0] in ["DOUBLELITERAL", "FLOATLITERAL"]:
					afterStrList.append("INTLITERAL")
				else:
					afterStrList.append(token[0])
				#print token[1]
		#print len(beforeStrList)
		#print len(afterStrList)
		
		print beforeF
		print afterF
		s = difflib.SequenceMatcher(None,a='', b='',autojunk=False)
		s.set_seqs(beforeStrList, afterStrList)
		#assert len(s.get_opcodes()) > 3
		if len(s.get_opcodes()) > 3:
			for opcode in s.get_opcodes():
				print opcode
				
				#print beforeStrList[opcode[1]]
				print beforeToks[opcode[1]]
				print beforeToks[opcode[3]]
				print "-----------"
			
			print type(radha)
		
	

		#sys.exit()
	print "FINISHED"

	#getToks = java.lex(toCompTokD)

	
if __name__ == '__main__':
	getCol()
