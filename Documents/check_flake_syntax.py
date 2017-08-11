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

# Takes in a string of Python code and checks for errors
# NOTE: FOR FLAKE8

import os
import subprocess
import sys
import tempfile
from compile_error import CompileError

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle.encode())
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start	

# Main method
def checkFlakeSyntax(src):
		myFile = open("toCheck.py", "w")
		myFile.write(src)
		myFile.close()
		proc = subprocess.Popen(['flake8', 'toCheck.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stream, err = proc.communicate()
		rc = proc.returncode
		errorFlag = find_nth(stream, 'SyntaxError:', 1)
		if rc == 0:
			# No errors, all good
			os.remove("toCheck.py")
			return None
		elif errorFlag < 0:
			# No errors, all good
			os.remove("toCheck.py")
			return None
		else:
			# Error, disect data for constructor	
			colonFirInd = find_nth(stream, ':', 1)

			fileName = stream[:colonFirInd]
			errorInd = find_nth(stream, 'SyntaxError:', 1)
			errorname = "SyntaxError".encode()

			temp1 = stream[errorInd:]
			cutOffInd = find_nth(temp1, fileName.decode(), 1)
			
			text = temp1[13:cutOffInd-1]
			
			temp2 = stream[:errorInd-5]
	
			colInd = temp2.rfind(':'.encode())
			midInd = temp2.rfind(':'.encode(), 0, colInd)
			linInd = temp2.rfind(':'.encode(), 0, midInd)
			column = int(temp2[midInd+1:colInd])
			line = int(temp2[linInd+1:midInd])

			errorObj = CompileError(fileName, line, column, None, text, errorname)
			os.remove("toCheck.py")
			return [errorObj]

