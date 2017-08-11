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

from check_v8_syntax import checkV8Syntax
from compile_error import CompileError

import unittest

ERROR_TEST = """if (process.argv.length < 3)
	console.error("not enough args");
	process.exit(1);
}
"""

class TestStringMethods(unittest.TestCase):

	def test_syntax_ok(self):
		toTest = checkV8Syntax('a=1+2')
		self.assertTrue(toTest is None)
		
	def test_syntax_error(self):
		toTest = checkV8Syntax(ERROR_TEST)
		self.assertTrue(isinstance (toTest[0], CompileError))
		self.assertEqual(toTest[0].filename, 'toCheck.js')
		self.assertEqual(toTest[0].line, 4)
		self.assertEqual(toTest[0].column, None)
		self.assertEqual(toTest[0].functionname, None)
		self.assertEqual(toTest[0].text, 'Unexpected token }')
		self.assertEqual(toTest[0].errorname, 'SyntaxError')
	
		
if __name__ == '__main__':
    unittest.main()
