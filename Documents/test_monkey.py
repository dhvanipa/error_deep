from check_monkey_syntax import checkMonkeySyntax
from compile_error import CompileError

import unittest

ERROR_TEST = """if (process.argv.length < 3)
	console.error("not enough args");
	process.exit(1);
}
"""

class TestStringMethods(unittest.TestCase):

	def test_syntax_ok(self):
		toTest = checkMonkeySyntax('a=1+2')
		self.assertTrue(toTest is None)
		
	def test_syntax_error(self):
		toTest = checkMonkeySyntax(ERROR_TEST)
		self.assertTrue(isinstance (toTest[0], CompileError))
		self.assertEqual(toTest[0].filename, 'toCheck.js')
		self.assertEqual(toTest[0].line, 4)
		self.assertEqual(toTest[0].column, 0)
		self.assertEqual(toTest[0].functionname, None)
		self.assertEqual(toTest[0].text, 'syntax error: }')
		self.assertEqual(toTest[0].errorname, 'SyntaxError')
	
		
if __name__ == '__main__':
    unittest.main()
