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
# NOTE: FOR V8
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
def checkV8Syntax(src):
		myFile = open("toCheck.js", "w")
		myFile.write(src)
		myFile.close()
		proc = subprocess.Popen(['node', '-c', 'toCheck.js'], stderr=subprocess.PIPE)
		streamdata, err = proc.communicate()
		rc = proc.returncode
		if rc == 0:
			# No errors, all good
			os.remove("toCheck.js")
			return None
		else:
			
			proc = subprocess.Popen(['v8/out.gn/x64.release/d8', 'toCheck.js'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stream, err = proc.communicate()
			# Error, disect data for constructor	
			colonFirInd = find_nth(stream, ':', 1)
			colonSecInd = find_nth(stream, ':', 2)	
			colonThirInd = find_nth(stream, ':', 3)		
			endInd = find_nth(stream, ' ', 1)	

			fileName = stream[0:colonFirInd]
			line = int(stream[colonFirInd+1:colonSecInd])
			
			
			errorname = stream[endInd+1:colonThirInd]

			nextName = find_nth(stream, errorname, 2)

			temp = stream[nextName+2:]
			tempcolId = find_nth(temp, ':', 1)			
			text = temp[tempcolId+2:]
			text = text.strip()

			errorObj = CompileError(fileName, line, None, None, text, errorname)
			os.remove("toCheck.js")
			return [errorObj]		

