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
# NOTE: FOR ECLIPSE

import os
import subprocess
import sys
import tempfile
from compile_error import CompileError
import pdb

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# Main method
def checkEclipseSyntax(src, flag_source):
		with open(src) as f:
      		  for i, l in enumerate(f):
            		pass
  		numTotLines = i + 1

		with open (src, "r") as myfile:
   			data = myfile.read()
		#print data
		myFile = open("ToCheckEc.java", "w")
		myFile.write(data)
		myFile.close()
		if flag_source == False:
			proc = subprocess.Popen(['java', '-jar', '../Downloads/ecj-4.7.jar', 'ToCheckEc.java', '-maxProblems', '500', '-source', '1.8', '-nowarn'], stderr=subprocess.PIPE)
		elif flag_source == True:
			proc = subprocess.Popen(['java', '-jar', '../Downloads/ecj-4.7.jar', 'ToCheckEc.java',  '-maxProblems', '500', '-nowarn'], stderr=subprocess.PIPE)
		streamdata, err = proc.communicate()
		rc = proc.returncode
		if rc == 0:
			# No errors, all good
			os.remove("ToCheckEc.java")
			return None
		else:
			# Error, disect data for constructor		
			#print err
			err = err[:len(err)-1]
			print err
			#data = data[1:]
			lastLine = err.rfind("\n")
			#print lastLine
			#print "split"
			#print len(err)
			lastErrorNum = err[lastLine:]
			cutOff = find_nth(lastErrorNum, '(', 1)
			lastError = lastErrorNum[cutOff+1:lastErrorNum.index('error')-1]
			numError = int(lastError)
			
			
			lineNums = []
			insToks = []
			indRepeats = []
			typeErrors = []
			colNums = []
			flagError = False
			for ind in range(numError):
				flagError = True
				#print numError
				fileInd = find_nth(err, "(at line ", ind+1)
				temp = err[fileInd:]
				#print "OK"
				#print temp
				data = data.replace("\t", "        ")
				firLnBr = find_nth(temp, "\n", 1)
				secLnBr = find_nth(temp, "\n", 2)
				actualLineBef = temp[firLnBr+1:secLnBr]
				#print data

				cutColInd = find_nth(temp, ")", 1)
				line = err[fileInd+9:cutColInd+fileInd]
				
				#print "-"
				#srcInd = data.index(actualLineBef.strip())


				#srcLineBefore = data[:srcInd]
				#cutSrc = srcLineBefore.rfind("\n")
				#actualLine = data[cutSrc+1:srcInd+len(actualLineBef)-1]
				#print actualLine
				#print "done"
				colLine = temp[secLnBr+1:]
				#print actualLineBef
				#pdb.set_trace()
				if int(line) != 1:
					actualLine = data[find_nth(data, "\n", int(line)-1)+1:find_nth(data, "\n", int(line))]	
					#print data[:find_nth(data, "\n", int(line))]
				else:
					actualLine = data[:find_nth(data, "\n", int(line))]	
				
				#letsFind = 1
				#lastCol = find_nth(colLine, "^",1)
				otherFlagInd = find_nth(colLine, "\n", 1)
				cutMore = colLine[:otherFlagInd]
				#firstCol = firstCol-2
				cutMore = cutMore[1:]
				cutMore = cutMore.replace("\t", "        ")

				
				#print indFirstR
				actualLine = actualLine.decode('utf-8')
				#print actualLine
				actualLine = actualLine.replace("\t", "        ")

				diff = len(actualLine) - len(actualLineBef) + 1
				#print diff
				#print cutMore
				for _ in range(diff):
					cutMore = " " + cutMore
				#print actualLine
				#print cutMore
				

				aFirstCol = find_nth(cutMore, "^",1)
				#print cutMore
				#print actualLine
				cutToFirst = actualLine[:aFirstCol]
				#print cutMore
				indFirstR = 0
				for c in reversed(cutToFirst):
					if c != ' ':
						break
					indFirstR +=1
				#print len(cutToFirst)

				#print "---"
				#print repr(cutToFirst)
				#print cutToFirst
				#print indFirstR
				#print "---"
				firstCol = len(cutToFirst) - indFirstR - 1


				#print len(cutToFirst)
				#print "marker"
				#print firstCol
				if len(cutToFirst) == 0:
					firstCol = aFirstCol - 1
				elif len(cutToFirst) == indFirstR:
					firstCol = indFirstR - 1
	
				#print actualLine
				aLastCol = cutMore.rfind("^")
				cutToLast = actualLine[aLastCol+1:]
				#print cutToLast
				indLast = 0
				for c in cutToLast:
					#print c
					if c != ' ':
						break
					indLast +=1
				#print aLastCol
				lastCol = indLast+aLastCol+1
				#print actualLine
				#print cutMore
				#print actualCol
				#print "YAY"		
				#print actualLine
				if len(actualLine) == 1:
					#print "here"
					firstCol = 0
					lastCol = 0
				before = len(insToks)
				#print before
				synErrInd = find_nth(temp, "Syntax error", 1)
				flagInd = find_nth(temp, "----------\n", 1)
				#print flagError
				#print flagInd
				if synErrInd != -1 and synErrInd < flagInd:
					actLine = temp[synErrInd:]
					tokInsInd = find_nth(actLine, ", insert", 1)
					#print tokInsInd
					#print "dhvani"
					if tokInsInd != -1 and (tokInsInd+synErrInd) < flagInd:
						#print "HERE TOO"
						cut = find_nth(actLine, "\" ", 1)
						typeErrors.append('i')
						toksIns = actLine[tokInsInd+10:cut]
						#print toksIns
						insToks.append(toksIns)
						flagError = True

				stringInd = find_nth(temp, "String literal is not properly closed by a double-quote", 1)
				if stringInd != -1 and stringInd < flagInd:
					typeErrors.append('i')
					toksIns = "\""
					insToks.append(toksIns)
					flagError = True
				subErrInd = find_nth(temp, "Syntax error on token", 1)
				if subErrInd != -1 and subErrInd < flagInd:
					cutLine = temp[subErrInd:]
					fixTok = find_nth(cutLine, "expected after this token", 1)
					if fixTok != -1 and (subErrInd + fixTok) < flagInd:
						cutInd = find_nth(cutLine,"\", ", 1)
						toksSub = cutLine[cutInd+3:fixTok-1] 
						typeErrors.append('i')
						insToks.append(toksSub)
						flagError = True
					if fixTok == -1:
						fixTokCheck = find_nth(cutLine, "expected before this token", 1)
						if fixTokCheck != -1 and (fixTokCheck + subErrInd) < flagInd:
							cutInd = find_nth(cutLine,"\", ", 1)
							toksSub = cutLine[cutInd+3:fixTokCheck-1] 
							typeErrors.append('i')
							insToks.append(toksSub)	
							flagError = True		
						if fixTokCheck == -1:
							checkSub = find_nth(cutLine, "expected", 1)
							if checkSub != -1 and (checkSub  + subErrInd)< flagInd:
								#print "HERE"
								cutInd = find_nth(cutLine,"\", ", 1)
								toksSub = cutLine[cutInd+3:checkSub-1] 
								typeErrors.append('s')
								insToks.append(toksSub)	
								#print toksSub
								flagError = True
					delInd = find_nth(cutLine, ", delete this token", 1)	
					if delInd != -1 and (delInd + subErrInd) < flagInd:
						delTok = temp[subErrInd+23:subErrInd+delInd-1]
						typeErrors.append('d')
						insToks.append(delTok)
						flagError = True
				mulErrInd = find_nth(temp, "Syntax error on tokens, delete these tokens", 1)
				if mulErrInd != -1 and mulErrInd < flagInd:
					typeErrors.append('d')
					insToks.append('')	
					#print toksSub
					flagError = True
				fakeInd = find_nth(temp, "cannot be resolved", 1)
				fakeTwoInd = find_nth(temp, "is undefined", 1)
				if fakeInd != -1 and fakeInd < flagInd:
					flagError = False
				if fakeTwoInd != -1 and fakeTwoInd < flagInd:
					flagError = False
		
				#print flagError
				sourceCheckInd = find_nth(temp, "are only available if source level is 1.5 or greater", 1)
				if sourceCheckInd != -1 and sourceCheckInd < flagInd:
					#print "here"
					#print temp
					flagError = False
				#print before
				#print insToks
				checkAsserInd = temp.find("must be defined in its own file")	
				#print checkAsserInd
				#print flagInd
				if checkAsserInd == -1 or checkAsserInd > flagInd:
					#print "HERE-------------------------------------------------------------"
					if len(insToks) != before+1:
						bruhFakeCheck = find_nth(temp, "type", 1)
						if bruhFakeCheck == -1:
							bruhFakeCheck = find_nth(temp, "Type", 1)
						if bruhFakeCheck != -1 and bruhFakeCheck < flagInd:
							#print "?"
							realCheck = find_nth(temp, "is out of range", 1)
							realTwoCheck = find_nth(temp, "Incorrect number of arguments", 1)
							comeCheck = find_nth(temp, "void is an invalid type for the", 1)
							anotCheck = find_nth(temp, "only final is permitted", 1)
							randCheck = find_nth(temp, "invalid TypeDeclaration", 1)
							andCheck = find_nth(temp, "must provide either dimension expressions or an array initializer", 1)
							synCheck = find_nth(temp, "Syntax error on token", 1)
							if realCheck != -1 and realCheck < flagInd:
								flagError = True
							elif realTwoCheck != -1 and realTwoCheck < flagInd:
								flagError = True
							elif comeCheck != -1 and comeCheck < flagInd:
								flagError = True
							elif anotCheck != -1 and anotCheck < flagInd:
								flagError = True
							elif randCheck != -1 and randCheck < flagInd:
								flagError = True
							elif andCheck != -1 and andCheck < flagInd:
								flagError = True
							elif synCheck != -1 and synCheck < flagInd:
								flagError = True
							else:
								flagError = False
						#print flagError
						anotherFlag = find_nth(temp, "Return type", 1)
						if anotherFlag != -1 and anotherFlag < flagInd:
							flagError = True
						if flagError == True:
							#print "dhvani"
							typeErrors.append('')
							insToks.append('')	
						
				#print flagError
				if flagError == True:
					cutColInd = find_nth(temp, ")", 1)
					line = err[fileInd+9:cutColInd+fileInd]
					lineNums.append(int(line))
					#print "-__-__-__-"
					#print firstCol
					#assert firstCol != -1
					#assert lastCol != -1
					colNums.append([firstCol, lastCol])
				

			#print insToks
			#print insToks
			#print lineNums
			#print "----OUT----"
			checkInd = err.find("must be defined in its own file")
			#print msgNo
			#print lineNums
			if checkInd != -1:
				check = err[:checkInd]
				lastCheck = check.rfind("(at line ")
				tempR = err[lastCheck:]
				cutColInd = find_nth(tempR, ")", 1)
				lineRemov = err[lastCheck+9:cutColInd+lastCheck]
				rid = int(lineRemov)
				goOver = lineNums[:]	
				flag = False		
				for x in goOver:
					if x == rid and flag == False:
						del colNums[lineNums.index(rid)]
						lineNums.remove(rid)
						flag = True

			checkIndAgain = find_nth(err, 'must be defined in its own file', 2)
			count = 2
			while checkIndAgain != -1:
				check = err[:checkIndAgain]
				lastCheck = check.rfind("(at line ")
				tempR = err[lastCheck:]
				cutColInd = find_nth(tempR, ")", 1)
				lineRemov = err[lastCheck+9:cutColInd+lastCheck]
				rid = int(lineRemov)
				goOver = lineNums[:]	
				flag = False		
				for x in goOver:
					if x == rid and flag == False:
						del colNums[lineNums.index(rid)]
						lineNums.remove(rid)
						flag = True
				count += 1
				checkIndAgain = find_nth(err, 'must be defined in its own file', count)
		
			msgNo = []
			for x in range(len(lineNums)):
				msgNo.append(x+1)

			#print msgNo
			#print lineNums
		
			if len(msgNo) == 0 and len(lineNums) == 0:
				os.remove("ToCheckEc.java")
				#return numTotLines, [0], [0], [''], ['']
				#print "Here"
				#print flag_source
				if flag_source == True:
					return numTotLines, [0], [0], [''], [''], [-1,-1]
				else:
					#print "important"
					return checkEclipseSyntax(src, True)


			else:
				#errorObj = CompileError(fileName, line, column, None, text, errorname)
				#print err
				print msgNo
				print lineNums
				print typeErrors
				print insToks
				print colNums
				#print len(msgNo)
				#print len(lineNums)
				#print len(insToks)
				#print len(typeErrors)	
				os.remove("ToCheckEc.java")
				assert len(msgNo) == len(lineNums) == len(typeErrors) == len(insToks) == len(colNums)
				return numTotLines, msgNo, lineNums, insToks, typeErrors, colNums

	

if __name__ == '__main__':
	inputFile = sys.argv[1]
	checkEclipseSyntax(inputFile, False)
					
