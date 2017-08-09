#!/usr/bin/python
#    Copyright 2017 Dhvani Patel
#
#    This file is part of UnnaturalCode.
#    
#    UnnaturalCode is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    UnnaturalCode is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with UnnaturalCode.  If not, see <http://www.gnu.org/licenses/>.

# Takes in a string of Java code and checks for errors
# NOTE: FOR JAVAC

import os
import subprocess
import sys
import tempfile
from compile_error import CompileError

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# Main method
def checkJavaCSyntax(src):
		with open(src) as f:
      		  for i, l in enumerate(f):
            		pass
  		numTotLines = i + 1

		with open (src, "r") as myfile:
   			data = myfile.read()
		#print data
		myFile = open("ToCheck.java", "w")
		myFile.write(data)
		myFile.close()
		proc = subprocess.Popen(['javac', 'ToCheck.java', '-nowarn'], stderr=subprocess.PIPE)
		streamdata, err = proc.communicate()
		rc = proc.returncode
		if rc == 0:
			# No errors, all good
			os.remove("ToCheck.java")
			return None
		else:
			# Error, disect data for constructor		
			#print err
			err = err[:len(err)-1]
			#print err
			
			lastLine = err.rfind("\n")
			#print lastLine
			#print "split"
			#print len(err)
			lastErrorNum = err[lastLine:]
			#print lastErrorNum
			lastError = lastErrorNum[:lastErrorNum.index('error')-1]
			numError = int(lastError)
			
			
			lineNums = []
			insToks = []
			indRepeats = []
			indRepeatsB = []
			typeErrors = []
			origLineNums = []	
			origLineNumsB = []
			flag = False
			flagB = False
			ind = 0
			for ind in range(numError):
				fileInd = find_nth(err, "ToCheck.java:", ind+1)
				temp = err[fileInd:]
				#print "ok"
				#print temp
				firstNewLine = find_nth(temp, "\n", 1)
				firstLine = temp[:firstNewLine]
				#print firstLine
				#temp = temp[:firstNewLine]
				errorColInd = find_nth(firstLine, "error:", 1)
				expectInd = find_nth(firstLine, "expected", 1)
				#print expectInd
				if expectInd != -1:
					#print expectInd
					typeErrors.append('i')
					beforeS = firstLine[errorColInd+7:errorColInd+8]
					afterS = firstLine[expectInd-2:expectInd-1]
					if beforeS == '\'' and afterS == '\'':
						insTok = firstLine[errorColInd+8:expectInd-2]
					else:
						insTok = firstLine[errorColInd+7:expectInd-1]
					if insTok == "class, interface, or enum":
						flag = True
						flagB = False
						insToks.append("class")
						insToks.append("interface")
						insToks.append("enum")
						typeErrors.append('i')
						typeErrors.append('i')
					elif insTok == "(\' or \'[":
						flagB = True
						flag = False
						insToks.append("(")
						insToks.append("[")
						typeErrors.append('i')
					else:
						flag = False
						flagB = False
						insToks.append(insTok)
			
				else:
					flag = False
					flagB = False
					typeErrors.append('')
					insToks.append('')
				cutColInd = find_nth(temp, ":", 2)
				line = err[fileInd+13:cutColInd+fileInd]
				#print flag
				if flag == True:
					#print int(line)
					lineNums.append(int(line))
					origLineNums.append(int(line))
					#indRepeats.append(origLineNums.index(int(line)))
					indRepeats.append(ind)
					lineNums.append(int(line))
				if flagB == True:
					lineNums.append(int(line))
					origLineNumsB.append(int(line))
					indRepeatsB.append(ind)
					#indRepeatsB.append(origLineNumsB.index(int(line)))
				else:
					origLineNums.append(int(line))	
					origLineNumsB.append(int(line))
				lineNums.append(int(line))
				ind += 1
			#print lineNums	
			#print origLineNums
			#print "RADHA"	
			#print indRepeatsB
			#print "----OUT----"
			checkInd = err.find("is public, should be declared in a file named")
			#print msgNo
			#print lineNums
			if checkInd != -1:
				check = err[:checkInd]
				lastCheck = err.rfind("ToCheck.java:")
				tempR = err[lastCheck:]
				cutColInd = find_nth(tempR, ":", 2)	
				lineRemov = err[lastCheck+13:cutColInd+lastCheck]
				rid = int(lineRemov)
				goOver = lineNums[:]			
				for x in goOver:
					if x == rid:
						lineNums.remove(rid)
			msgNo = []
			#print indRepeatsB
			msgNoInd = 0
			#print 
			for x in range(len(lineNums) - (( (len(indRepeats)*2) + (len(indRepeatsB)) ) )):
				#print x
				if x in indRepeats:
					#print "TRUE"
					msgNo.append(msgNoInd+1)
					msgNo.append(msgNoInd+2)	
					msgNo.append(msgNoInd+3)
					msgNoInd += 3
				elif x in indRepeatsB:
					msgNo.append(msgNoInd+1)			
					msgNo.append(msgNoInd+2)
					msgNoInd += 2
				else:
					msgNo.append(msgNoInd+1)
					msgNoInd += 1
				#print msgNo
				

			#print msgNo
			#print lineNums
			

			if len(msgNo) == 0 and len(lineNums) == 0:
				#os.remove("ToCheck.java")
				return None
			else:
				#errorObj = CompileError(fileName, line, column, None, text, errorname)
				print err
				print msgNo
				print lineNums
				print insToks
				print typeErrors
				#print len(msgNo)
				#print len(lineNums)
				#print len(insToks)
				#print len(typeErrors)	
				os.remove("ToCheck.java")
				return numTotLines, msgNo, lineNums, insToks, typeErrors	


if __name__ == '__main__':
	inputFile = sys.argv[1]
	checkJavaCSyntax(inputFile)

