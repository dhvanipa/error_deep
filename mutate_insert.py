# Copyright 2017 Dhvani Patel

import json
from pprint import pprint
import tokenize
from check_pypy_syntax import checkPyPySyntax
from compile_error import CompileError
import token
from Token import Token
from random import randint

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle.encode())
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def insertMut(raw_text):
	with open('vocabulary_mutate.json') as data_file:    
    		data = json.load(data_file)
		pprint(data)
		print "HI"

	chosenInd = randint(0,86)
	chosenToken = data["indexes_m"][chosenInd]
	print chosenToken

	raw_text = str(raw_text)
	num_lines = raw_text.count('\n')+1

	chosenLineInd = randint(1,num_lines)
	print chosenLineInd

	if chosenLineInd == 1:
		first_strip = raw_text[:find_nth(raw_text, "\n", chosenLineInd)]
	else:
		first_strip = raw_text[find_nth(raw_text, "\n", chosenLineInd-1)+1:find_nth(raw_text, "\n", chosenLineInd)]
	print len(first_strip)
	print first_strip

	chosenColInd = randint(1,len(first_strip)+2)

	first_col_strip = first_strip[:chosenColInd]
	last_col_strip = first_strip[chosenColInd:]
	new_line = first_col_strip + chosenToken + last_col_strip
	print new_line


	if chosenLineInd ==1 :
		print "F"
		last_text = raw_text[find_nth(raw_text, "\n", chosenLineInd)+1:]
		print "L"
		print last_text
		final_code_text = new_line + "\n" + last_text

	elif chosenLineInd == num_lines:
		first_text = raw_text[:find_nth(raw_text, "\n", chosenLineInd-1)]
		print "F"
		print first_text

		final_code_text = first_text + "\n" + new_line
	
	else:
		first_text = raw_text[:find_nth(raw_text, "\n", chosenLineInd-1)]
		print "F"
		print first_text

		last_text = raw_text[find_nth(raw_text, "\n", chosenLineInd)+1:]
		print "L"
		print last_text

		final_code_text = first_text + new_line.encode() + "\n" + last_text


	
	print '------------------------------------'
	print final_code_text


	print num_lines

	toTest = checkPyPySyntax(final_code_text)

	if toTest == None:
 		print "Try again..."	
		insertMut(raw_text)
	else:
		print toTest[0]
		print toTest[0].filename
		print toTest[0].line
		print toTest[0].column
		print toTest[0].functionname
		print toTest[0].text
		print toTest[0].errorname
	
	print "-----------FINISHED-------------------"

