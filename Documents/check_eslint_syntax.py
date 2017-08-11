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

# Takes in a string of JavaScript code and checks for errors
# NOTE: FOR ESLINT

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
def checkEslintSyntax(src):
		myFile = open("toCheck.js", "w")
		myFile.write(src)
		myFile.close()
		proc = subprocess.Popen(['../node_modules/.bin/eslint', 'toCheck.js', '--no-color', '--quiet', '-f', 'tap'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stream, err = proc.communicate()
		rc = proc.returncode
		if rc == 0:
			# No errors, all good
			os.remove("toCheck.js")
			return None
		else:
			# Error, disect data for constructor
			lineInd = find_nth(stream, 'line:', 1)
			colInd = find_nth(stream, 'column:', 1)
			errorInd = find_nth(stream, 'severity:', 1)
			messageInd = find_nth(stream, 'message:', 1)
			fileInd = find_nth(stream, '.js', 1)
			ruleInd = find_nth(stream, 'ruleId:', 1)
			dataInd = find_nth(stream, 'data:', 1)	
			startInd = find_nth(stream, 'not ok', 1)	

			temp = stream[startInd:fileInd+3]
			cutInd = temp.rfind('/')
				
			fileName = stream[startInd+cutInd+1:fileInd+3]

			line = int(stream[lineInd+6:colInd-5])
			column = int(stream[colInd+8:ruleInd-5])

			errorname = stream[errorInd+10:dataInd-3]

			text = stream[messageInd+10:errorInd-4]
			
			errorObj = CompileError(fileName, line, column, None, text, errorname)
			os.remove("toCheck.js")
			return [errorObj]		

