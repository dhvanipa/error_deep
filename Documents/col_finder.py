import csv
import os
from javac_parser import Java
from io import open
import sys
import keyword
import difflib

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

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

	all_cols = []
	
	csvfile = open('java_fixes_col.csv', 'wb')
	datWriter = csv.writer(csvfile, delimiter=',',
                        	   quoting=csv.QUOTE_MINIMAL)
	datWriter.writerow(["sfid", "meid", "line_start", "col_start", "line_end", "col_end"])
	for loopInd in range(len(strPathsBef)):	
		beforeLen = len(all_cols)
		#print loopInd
		if loopInd == 2784:
			continue
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
				elif token[0] == "CHARLITERAL":
					beforeStrList.append("STRINGLITERAL")
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
				elif token[0] == "CHARLITERAL":
					afterStrList.append("STRINGLITERAL")
				else:
					afterStrList.append(token[0])
				#print token[1]
		#print len(beforeStrList)
		#print len(afterStrList)
		sfid = int(beforeF[find_nth(beforeF, "/", 4)+1:find_nth(beforeF, "/", 5)])
		meid = int(beforeF[find_nth(beforeF, "/", 5)+1:find_nth(beforeF, "/", 6)])
		#print beforeF
		#print afterF
		s = difflib.SequenceMatcher(None,a='', b='',autojunk=False)
		s.set_seqs(beforeStrList, afterStrList)
		#assert len(s.get_opcodes()) > 3
	
		for opcode in s.get_opcodes():
			#print opcode
			if opcode[0] != "equal":
				if opcode[0] != "delete":
					#print type(beforeToks[opcode[3]][2])
					add = [sfid, meid, beforeToks[opcode[3]][2][0],beforeToks[opcode[3]][2][1], beforeToks[opcode[3]][3][0], beforeToks[opcode[3]][3][1]]
					#print add
					datWriter.writerow(add)
					break
				else:
					#print type(beforeToks[opcode[1]][2])
					add = [sfid, meid, beforeToks[opcode[1]][2][0],beforeToks[opcode[1]][2][1], beforeToks[opcode[1]][3][0], beforeToks[opcode[1]][3][1]]
					datWriter.writerow(add)
					break

		#print all_cols
		#print type(radha)
	

		#sys.exit()
	csvfile.close()
	print "FINISHED"
	#print all_cols

	#getToks = java.lex(toCompTokD)

	
if __name__ == '__main__':
	getCol()
