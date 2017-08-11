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


from check_javac_syntax import checkJavaCSyntax
from compile_error import CompileError

import unittest

ERROR_TEST = """public class HelloWorld {

    public static void main(String[] args)
        // Prints "Hello, World" to the terminal window.
        System.out.println("Hello, World)
    }

}
"""

class TestStringMethods(unittest.TestCase):

	def test_syntax_ok(self):
		toTest = checkJavaCSyntax('public class Hello{ int a= 5;}')
		self.assertTrue(toTest is None)
		
	def test_syntax_error(self):
		toTest = checkJavaCSyntax(ERROR_TEST)
		self.assertEqual(toTest[0], [1, 2, 3])
		self.assertEqual(toTest[1], [3, 5, 8])
	
		
if __name__ == '__main__':
    unittest.main()
