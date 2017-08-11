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
# NOTE: FOR BABEL

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
def checkBabelSyntax(src):
		myFile = open("toCheck.js", "w")
		myFile.write(src)
		myFile.close()
		proc = subprocess.Popen(['node_modules/.bin/babel', 'toCheck.js', '-o', '/dev/null', '--no-highlight-code'], stderr=subprocess.PIPE)
		streamdata, err = proc.communicate()
		rc = proc.returncode
		if rc == 0:
			# No errors, all good
			os.remove("toCheck.js")
			return None
		else:
			# Error, disect data for constructor		
			colonFirInd = find_nth(err, ':', 1)
			colonSecInd = find_nth(err, ':', 2)
			colonThirInd = find_nth(err, ':', 3)		
			lineBegin = find_nth(err, '(', 1)		
			lineEnd = find_nth(err, ')', 1)	

			fileName = err[colonFirInd+2:colonSecInd]
			line = int(err[lineBegin+1:colonThirInd])
			column = int(err[colonThirInd+1:lineEnd])

			errorname = err[0:colonFirInd]

			flagStart = find_nth(err, '>', 1)
			flagEnd = find_nth(err, '^', 1)
			

			#temp = err[flagStart:]
			#ind = find_nth(temp, '\n', 1)

			textBefore = err[colonSecInd+2:lineBegin-1]
			textAfter = err[flagStart+6:flagEnd-7]
			text = textBefore + ' ' + textAfter
			
			errorObj = CompileError(fileName, line, column, None, text, errorname)
			os.remove("toCheck.js")
			return [errorObj]	

