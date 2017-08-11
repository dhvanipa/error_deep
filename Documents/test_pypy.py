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


from check_pypy_syntax import checkPyPySyntax
from compile_error import CompileError

import unittest

ERROR_TEST = """# -*- coding: utf-8 -*-
'''
External pillar module for testing the contents of __opts__ as seen
by external pillar modules.

Returns a hash of the name of the pillar module as defined in
_virtual__ with the value __opts__
'''

# Import python libs
from __future__ import absolute_import
import logging

# Set up logging
log = logging.getLogger(__name__)

# DRY up the name we use
MY_NAME = 'test_ext_pillar_opts'


def __virtual__():    log.ebug('Loaded external pillar {0} as {1}'.format(__name__, MY_NAME))
    return True


def ext_pillar(minion_id, pillar, *args):
    return {MY_NAME: __opts__}


"""

class TestStringMethods(unittest.TestCase):

	def test_syntax_ok(self):
		toTest = checkPyPySyntax('a=1+2')
		self.assertTrue(toTest is None)
		
	def test_syntax_error(self):
		toTest = checkPyPySyntax(ERROR_TEST)
		self.assertTrue(isinstance (toTest[0], CompileError))
		self.assertEqual(toTest[0].filename, 'toCheck.py'.encode())
		self.assertEqual(toTest[0].line, 1)
		self.assertEqual(toTest[0].column, None)
		self.assertEqual(toTest[0].functionname, None)
		self.assertEqual(toTest[0].text, 'unmatched \')\':if(true)):'.encode())
		self.assertEqual(toTest[0].errorname, 'SyntaxError'.encode())
	
		
if __name__ == '__main__':
    unittest.main()
