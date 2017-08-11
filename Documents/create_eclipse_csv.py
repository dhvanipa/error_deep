# Copyright 2017 Dhvani Patel

from check_eclipse_syntax import checkEclipseSyntax
import os
import csv

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def createEclipseCSV():
	rootdir = '/home/dhvani/java-mistakes-data'
	
	strPaths = []


	for subdir, dirs, files in os.walk(rootdir):
    		for file in files:
			path = os.path.join(subdir, file)
			if "mistakes.csv" not in path:
				if "after.java" not in path:
					#print path
					strPaths.append(path)

	#print strPaths[0]
	#print len(strPaths)
	csvfile = open('eclipse_fixes.csv', 'wb')
	datWriter = csv.writer(csvfile, delimiter=',')

	print "START"
	fileNum = 0

	for p in range(len(strPaths)):
			path = strPaths[p]
			print path
			#path = "/home/dhvani/java-mistakes-data/10038972/352572525/before.java"
			print fileNum + 1
			tool = "eclipse"
			sfid = path[find_nth(path, "/", 4)+1:find_nth(path, "/", 5)]
			meid = path[find_nth(path, "/", 5)+1:find_nth(path, "/", 6)]
			numTotLines, msgNo, lineNums, insToks, typeErrors, colNums = checkEclipseSyntax(path, False)
			#print numTotLines, msgNo, lineNums, insToks, typeErrors
			for ind in range(len(msgNo)):
				# HEADER: tool, sfid, meid, numTotLines, msgNo, lineNum, colStart, colEnd, typeError, fixToken
				toPut = [tool, sfid, meid, numTotLines, msgNo[ind], lineNums[ind], colNums[ind][0], colNums[ind][1], typeErrors[ind], insToks[ind]]
				datWriter.writerow(toPut)
			fileNum += 1
	csvfile.close()
	print "FINISH"
		

if __name__ == '__main__':
	createEclipseCSV()
