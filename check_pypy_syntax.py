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
# NOTE: FOR PYPY

import os
import subprocess
import sys
import tempfile
from compile_error import CompileError
import re

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle.encode())
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start	

# Main method
def checkPyPySyntax(src):
		myFile = open("toCheck.py", "w")
		myFile.write(src)
		myFile.close()
		proc = subprocess.Popen(['pypy', '-m', 'py_compile', 'toCheck.py'], stderr=subprocess.PIPE)
		streamdata, err = proc.communicate()
		rc = proc.returncode
		if rc == 0:
			# No errors, all good
			if os.path.isfile("toCheck.py") == True:
				os.remove("toCheck.py")
			return None
		else:
			# Error, disect data for constructor		
			fileBegInd = find_nth(err, 'File ', 1)
			fileEndInd = find_nth(err, ',', 1)
			lineInd = find_nth(err, 'line ', 1)

			nextLineInd = find_nth(err, '\n', 1)
		
		
			add = err[lineInd+5:nextLineInd]
			add = re.sub("[^0-9]", "", add)
			if(add == ''):
				add = '-1'
			line = int(add)

			textInd = find_nth(err, '    ', 1)
			temp2 = err[textInd+4:]
			
		
			nextLineIndTemp = find_nth(temp2, '    ', 1)
			textAfter = err[textInd+4:nextLineIndTemp+textInd+3]
			
			fileName = err[fileBegInd+6:fileEndInd-1]

			colon = ':'

			textBeforeInd = err.rfind(colon.encode())
			textBefore = err[textBeforeInd+2:]
			textBefore = textBefore.strip()
	
			colonTwo = ':'

			text = textBefore + colon.encode() + textAfter

			cutoffInd = find_nth(err, '^', 1)
			errorname = err[cutoffInd+2:textBeforeInd]
			
			errorObj = CompileError(fileName, line, None, None, text, errorname)
			if os.path.isfile("toCheck.py") == True:
				os.remove("toCheck.py")
			return [errorObj]


# Main method
def checkPyPySyntaxT(src):
		myFile = open("toCheck.py", "w")
		myFile.write(src.decode())
		myFile.close()
		proc = subprocess.Popen(['pypy', '-m', 'py_compile', 'toCheck.py'], stderr=subprocess.PIPE)
		streamdata, err = proc.communicate()
		rc = proc.returncode
		if rc == 0:
			# No errors, all good
			if os.path.isfile("toCheck.py") == True:
				os.remove("toCheck.py")
			return None
		else:
			# Error, disect data for constructor		
			fileBegInd = find_nth(err, 'File ', 1)
			fileEndInd = find_nth(err, ',', 1)
			lineInd = find_nth(err, 'line ', 1)

			nextLineInd = find_nth(err, '\n', 1)
		
		
			add = err[lineInd+5:nextLineInd]
			add = re.sub("[^0-9]", "", add.decode())
			if(add == ''):
				add = '-1'
			line = int(add)

			textInd = find_nth(err, '    ', 1)
			temp2 = err[textInd+4:]
			
		
			nextLineIndTemp = find_nth(temp2, '    ', 1)
			textAfter = err[textInd+4:nextLineIndTemp+textInd+3]
			
			fileName = err[fileBegInd+6:fileEndInd-1]

			colon = ':'

			textBeforeInd = err.rfind(colon.encode())
			textBefore = err[textBeforeInd+2:]
			textBefore = textBefore.strip()
	
			colonTwo = ':'

			text = textBefore + colon.encode() + textAfter

			cutoffInd = find_nth(err, '^', 1)
			errorname = err[cutoffInd+2:textBeforeInd]
			
			errorObj = CompileError(fileName, line, None, None, text, errorname)
			if os.path.isfile("toCheck.py") == True:
				os.remove("toCheck.py")
			return [errorObj]


