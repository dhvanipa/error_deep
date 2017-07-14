# Copyright 2017 Dhvani Patel

import json
from pprint import pprint
import tokenize
from check_pypy_syntax import checkPyPySyntax
from compile_error import CompileError
import token
from Token import Token
from random import randint

#Declaring Global Constants
YES_TOKEN = 0b00
NO_TOKEN = 0b01
INSERTION = 0b001
DELETION = 0b010
SUBSTITUTION = 0b100

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle.encode())
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def insertTokMut(raw_tokens, raw_text):

	with open('vocabulary_mutate.json') as data_file:    
    		data = json.load(data_file)
		pprint(data)
		print "HI"
	print len(data["indexes_m"])
	chosenInd = randint(0,84)
	chosenToken = data["indexes_m"][chosenInd]
	print chosenToken
	
	out_tokens_loc = []
	raw_tokens_pass = []
	orig = []
	for token in raw_tokens:
		token_use = token		
		orig.append(token_use)
		if token[0] != 5:
			if token[0] != 6:
				if token[0] != 4:
					if token[0] != 0:
						raw_tokens_pass.append(token_use)
						print token

	print "OKAY"
	
	
	
	num_lines = len(raw_tokens_pass)
	num_encode = len(orig)	

	chosenLineInd = randint(0, num_lines-1) #num_lines-1
	chosenTrueLineInd = -1
	indI = 0
	for x in orig:
		if raw_tokens_pass[chosenLineInd] == x:
			print "<3"
			chosenTrueLineInd = indI
			break
		indI = indI + 1
	print chosenTrueLineInd

	toIter = num_encode + (num_encode+1)
	for _ in range(toIter):
		out_tokens_loc.extend('0')

	lenD = len(out_tokens_loc)

	for indI in range(toIter):
		indLook = ((chosenTrueLineInd) * 2) + 1
		if indI == indLook+1:
			out_tokens_loc[indI] = ('1')

	source_code = raw_text

	print len(source_code)

	print raw_tokens_pass[chosenLineInd][0]


	print raw_tokens_pass[chosenLineInd][4]
	print raw_text
	toAddBeforeInd = source_code.index(raw_tokens_pass[chosenLineInd][4])

	
	temp = source_code[toAddBeforeInd:toAddBeforeInd+len(raw_tokens_pass[chosenLineInd][4])]
	print temp
	print "kobe"
	print raw_tokens_pass[chosenLineInd][1]

	shotInd = temp.index(raw_tokens_pass[chosenLineInd][1])

	change = temp.strip()
	check = temp.index(change)	
	print check

	print len(temp)
	print shotInd

	if shotInd+1 == len(temp):
		shotInd = shotInd-1

	actual_target_ind = toAddBeforeInd + shotInd


	before = source_code[:actual_target_ind+len(raw_tokens_pass[chosenLineInd][1])]
	print "B"
	print before
	
	after = source_code[actual_target_ind+len(raw_tokens_pass[chosenLineInd][1]):]
	print "A"
	print after	
	print raw_tokens_pass[chosenLineInd][0]

	if shotInd == 0:
		if raw_tokens_pass[chosenLineInd][0] == 4:
			new_text = before + chosenToken.encode() + after
		else:
			new_text = before + ' ' + chosenToken.encode() + ' ' + after
	else:
		if raw_tokens_pass[chosenLineInd][0] == 54:
			new_text = before + chosenToken.encode() + after
		
		elif chosenInd == data["indexes_m"].index('\n'): 
			print "shiz"
			if after[0] == ' ':
				space = ' ' * (check-1)
			else:
				space = ' ' * (check)
			new_text = before + chosenToken.encode() + space + after
		else:
			new_text = before + ' ' + chosenToken.encode() + ' ' + after
	print '------------------------------------'
	print new_text
	

	toTest = checkPyPySyntax(new_text)

	if toTest == None:
 		print "Try again..."	
		print "-----------FINISHED-------------------"
		#insertTokMut(raw_tokens_pass, raw_text)
		print "-----------FINISHED-------------------"
		print "shit man"
		lenR = 2
		lenK = 2
		return lenR, raw_tokens_pass, raw_text, lenK
	else:
		print "-----------FINISHED-------------------"
		print toTest[0]
		print toTest[0].filename
		print toTest[0].line
		print toTest[0].column
		print toTest[0].functionname
		print toTest[0].text
		print toTest[0].errorname
		print type(out_tokens_loc)
		print len(new_text)
		print NO_TOKEN
		print INSERTION
		print len(out_tokens_loc)
		return new_text, NO_TOKEN, INSERTION, out_tokens_loc
	
	print "-----------FINISHED-------------------"
	print chosenLineInd+1	
	print out_tokens_loc
	print len(raw_tokens_pass)
	print len(out_tokens_loc)
	print lenD
	print chosenTrueLineInd

