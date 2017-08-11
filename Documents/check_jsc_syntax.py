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
# NOTE: FOR JAVASCRIPT CORE (JSC)
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
def checkJSCSyntax(src):
		myFile = open("toCheck.js", "w")
		myFile.write(src)
		myFile.close()
		myCFile = open("code.js", "w")
		myCFile.write('checkSyntax(\'toCheck.js\')')
		myCFile.close()
		proc = subprocess.Popen(['WebKit/WebKitBuild/Release/bin/jsc', 'code.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stream, err = proc.communicate()
		rc = proc.returncode
		if rc == 0:
			# No errors, all good
			os.remove("toCheck.js")
			os.remove("code.js")
			return None
		else:
			colonFirInd = find_nth(stream, ':', 1)
			colonSecInd = find_nth(stream, ':', 2)
			fileInd = find_nth(stream, '.js', 1)
			checkInd = find_nth(stream, 'checkSyntax@', 1)
		
			temp = stream[:fileInd+3]
			cutInd = temp.rfind(' ')

			temp2 = stream[fileInd:]
			cut2Ind = find_nth(temp2, ':', 1)
			
			fileName = temp[cutInd+1:]
			
			text = stream[colonSecInd+2:cutInd-3]	

			line = int(stream[fileInd+cut2Ind+1:checkInd])

			errorname = stream[colonFirInd+2:colonSecInd]
	
			errorObj = CompileError(fileName, line, None, None, text, errorname)
			os.remove("toCheck.js")
			os.remove("code.js")
			return [errorObj]		

