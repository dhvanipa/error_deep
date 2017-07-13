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

def subTokMut(raw_tokens, raw_text):

	with open('vocabulary_mutate.json') as data_file:    
    		data = json.load(data_file)
		pprint(data)
		print "HI"

	chosenInd = randint(0,86)
	chosenToken = data["indexes_m"][chosenInd]
	print chosenToken
	
	raw_tokens_pass = []
	out_tokens_loc = []
	orig = []

	for token in raw_tokens:
		token_use = token		
		orig.append(token_use)
		if token[0] != 5:
			if token[0] != 6:
				if token[0] != 4:
					if token[0] != 54:
						if token[0] != 0:
							if token[0] != 53:
								raw_tokens_pass.append(token_use)
								#print token

	print "OKAY"
	
	num_lines = len(raw_tokens_pass)
	num_encode = len(orig)

	chosenLineInd = randint(0,3) # num_lines-1
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
		if indI == indLook:
			out_tokens_loc[indI] = ('1')

	source_code = raw_text

	send = Token(tokenize.tok_name[raw_tokens_pass[chosenLineInd][0]], raw_tokens_pass[chosenLineInd][1], raw_tokens_pass[chosenLineInd][2][0], raw_tokens_pass[chosenLineInd][2][1], raw_tokens_pass[chosenLineInd][3][0], raw_tokens_pass[chosenLineInd][3][1], raw_tokens_pass[chosenLineInd][4])

	indexToRemove = source_code.index(raw_tokens_pass[chosenLineInd][4])

	temp = source_code[indexToRemove:indexToRemove+len(raw_tokens_pass[chosenLineInd][4])+1]

	change = temp.strip()
	
	check = change.find(raw_tokens_pass[chosenLineInd][1])

	shotInd = temp.index(raw_tokens_pass[chosenLineInd][1])

	change = temp.strip()
	check = temp.index(change)
	print "WHAT"
	print change
	

	print "TEMP"
	print temp

	print shotInd
	
	actual_target_ind = indexToRemove + shotInd

	print raw_tokens_pass[chosenLineInd][1]
	
	print len(raw_tokens_pass[chosenLineInd][1])
	print len(change)

	if check == 0 and len(raw_tokens_pass[chosenLineInd][1]) == len(change):
		before = source_code[:indexToRemove]
	else:
		before = source_code[:actual_target_ind]
	print "B"
	print before
	
	
	after = source_code[actual_target_ind+len(raw_tokens_pass[chosenLineInd][1]):]
	print "A"
	print after	

	if check == 0:
		print "GOT EM"
		if after[0] == ' ':
			new_text = before + chosenToken.encode() + after
		else:
			new_text = before + chosenToken.encode() + after
	else:	
		
		if chosenInd == data["indexes_m"].index('\n'): 
			print "shiz"
			if after[0] == ' ':
				space = ' ' * (check-1)
			else:
				space = ' ' * (check)
			new_text = before + chosenToken.encode() + space + after
		else:
			print "WAS HERE"
			new_text = before + chosenToken.encode() + after


	print actual_target_ind

	print '-------------------------------'
	print new_text
	

	toTest = checkPyPySyntax(new_text)

	if toTest == None:
 		print "Try again..."	
		subTokMut(raw_tokens_pass, raw_text)
		return new_text, YES_TOKEN, SUBSTITUTION, out_tokens_loc, send
	else:
		print toTest[0]
		print toTest[0].filename
		print toTest[0].line
		print toTest[0].column
		print toTest[0].functionname
		print toTest[0].text
		print toTest[0].errorname
		return new_text, YES_TOKEN, SUBSTITUTION, out_tokens_loc, send
	
	print "-----------FINISHED-------------------"
	print chosenLineInd+1
	print out_tokens_loc
	print len(raw_tokens_pass)
	print len(out_tokens_loc)
	print lenD

