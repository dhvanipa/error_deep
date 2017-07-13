# Copyright 2017 Dhvani Patel

import sqlite3
from check_pypy_syntax import checkPyPySyntax
from compile_error import CompileError
import tokenize
import StringIO

# NUM TOTAL: 462 563
# / 3 = 154 187

def handle_token(type, token, (srow, scol), (erow, ecol), line):
    print "%d,%d-%d,%d:\t%s\t%s" % \
        (srow, scol, erow, ecol, tokenize.tok_name[type], repr(token))

def testTime():
	sqlite_file = "/home/dhvani/python-sources.sqlite3"
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()
	print "Success Connection to database..."
	c.execute("SELECT source FROM source_file INNER JOIN eligible_source ON source_file.hash = eligible_source.hash")
	print "Executed SELECT..."
	print "Fetching all rows..."
	all_rows = c.fetchmany(size=10)[0]
	print all_rows[0]	
	#for row in all_rows:
	#row = all_rows[0]	
	#print row[0], str(row[1]).encode('hex')
	print "Got Em..."
	print "Running PyPy test..."
	tokenize.tokenize(StringIO.StringIO(all_rows[0]).readline, handle_token)
	toTest = checkPyPySyntax(all_rows[0])
	print "DONE"
	if toTest == None:
		#output = ''
		#print output
		print "SUCCESS"
	else:
		print "Try again..."

if __name__ == '__main__':
    testTime()

