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
YES_TOKEN = 0b10
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

def deleteTokMutS(raw_tokens, all_tokens, raw_text):

	#out_tokens_loc = []
	raw_tokens_pass = []
	orig = []

	actual_token_len = []
	for token in all_tokens:
		token_use = token		
		#orig.append(token_use)
		actual_token_len.append(token_use)

	for token in raw_tokens:
		token_use = token		
		orig.append(token_use)

		raw_tokens_pass.append(token_use)
								#print token

	#print "OKAY"
	
	num_lines = len(actual_token_len)
	num_encode = len(orig)

	if (num_lines % 10 == 0):
		numTokensNeeded = int((num_lines / 10))
	else:
		numTokensNeeded = int((num_lines / 10))
	fixToks = []
	chosens = []
	
	haha = -1
	radOut = 0
	inds = []
	for i in actual_token_len:
		if i.type != 'COMMENT':
			if i.type != 'INDENT':
				if i.type != 'DEDENT':
					if i.type != 'NEWLINE':
						if i.type != 'NL':			
							if i.type != 'ENDMARKER':
								inds.append(actual_token_len.index(i))		
	#print inds
	#print len(inds)
	#print len(actual_token_len)
	#print type(radha)

	allInds = []
	for nah in range(numTokensNeeded+1):
		temp = []
		#print nah
		for nahHoi in range(len(inds)):
			if nah != 0:
				flag = nah * 10
				pastFlag = (nah-1)*10
				#print "inds"
				#print inds[nahHoi]
				#print "indsSSS"
				if pastFlag < inds[nahHoi] <= flag:	
					temp.append(inds[nahHoi])
		if len(temp) != 0:
			allInds.append(temp)
	
	#print allInds
	#print type(radha)
	#print len(allInds)
	#print numTokensNeeded
	curr = 0
	new_text = ''
	while radOut < len(allInds):

		if radOut == (numTokensNeeded-1):
			param_start = haha
			param_end = num_lines-1
		else:
			param_start = radOut * 10
			param_end = param_start + 9
			haha = param_end

		toChooseArr = allInds[radOut]
		
		chosenLineIndTemp = randint(0, len(toChooseArr)-1) #num_lines-1

		chosenLineInd = toChooseArr[chosenLineIndTemp]
		#print "ok"
		#print chosenLineInd
		chosens.append(chosenLineInd)
		#print radOut

		source_code = raw_text

		send = actual_token_len[chosenLineInd]
		#send = Token(tokenize.tok_name[raw_tokens_pass[chosenLineInd][0]], raw_tokens_pass[chosenLineInd][1], raw_tokens_pass[chosenLineInd][2][0], raw_tokens_pass[chosenLineInd][2][1], raw_tokens_pass[chosenLineInd][3][0], raw_tokens_pass[chosenLineInd][3][1], raw_tokens_pass[chosenLineInd][4])
		
		fixToks.append(send)
	
		indexToRemove = source_code.index(actual_token_len[chosenLineInd].line)
		#print actual_token_len[chosenLineInd].line

		temp = source_code[indexToRemove:indexToRemove+len(actual_token_len[chosenLineInd].line)+1]
		#print "temp"
		#print temp
		change = temp.strip()
		
		check = change.find(raw_tokens_pass[chosenLineInd][1])
		#print actual_token_len[chosenLineInd].value
		#print raw_tokens_pass[chosenLineInd][1]
	
		shotInd = temp.index(raw_tokens_pass[chosenLineInd][1])
		#print shotInd

		#print change
		
		#print "TEMP"
		#print temp

		#print shotInd
	
		actual_target_ind = indexToRemove + shotInd

		#print raw_tokens_pass[chosenLineInd][1]
	
		#print len(raw_tokens_pass[chosenLineInd][1])
		#print len(change)

		if check == 0 and len(raw_tokens_pass[chosenLineInd][1]) == len(change):
			before = source_code[:indexToRemove]
		else:
			before = source_code[:actual_target_ind]
		#print "B"
		#print before
	
	
		after = source_code[actual_target_ind+len(raw_tokens_pass[chosenLineInd][1]):]
		#print "A"
		#print after	

		if check == 0:
			#print "GOT EM"
			new_text = before + after[1:]
		else:	
			new_text = before + after
	
		#print actual_target_ind

		#print '-------------------------------'
		#print new_text
	

		toTest = checkPyPySyntax(new_text)
		if toTest == None:
			#print radOut
			#if radOut != 0:
			#	radOut = radOut-1
			#else:
			#	radOut = 0
			#print radOut	
			curr = curr + 1
			if curr > 10:
				radOut = radOut + 1
			else:
				radOut = radOut
				fixToks.remove(send)
				chosens.remove(chosenLineInd)
			#print "test_t"
		else:
			curr = 0
			radOut = radOut + 1


	
	return new_text, YES_TOKEN, DELETION, chosens, fixToks

def deleteTokMut(raw_tokens, raw_text):

	out_tokens_loc = []
	raw_tokens_pass = []
	orig = []

	for token in raw_tokens:
		token_use = token		
		orig.append(token_use)
		if token[0] != 5:
			if token[0] != 6:
				if token[0] != 4:
					if token[0] != 54:
						if token[0] != 53:
							if token[0] != 0:
								raw_tokens_pass.append(token_use)
								#print token

	#print "OKAY"
	
	num_lines = len(raw_tokens_pass)
	num_encode = len(orig)

	chosenLineInd = randint(0, num_lines-1) #num_lines-1
	chosenTrueLineInd = -1
	indI = 0
	for x in orig:
		if raw_tokens_pass[chosenLineInd] == x:
			#print "<3"
			chosenTrueLineInd = indI
			break
		indI = indI + 1
	#print chosenTrueLineInd


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
	#print change
	
	#print "TEMP"
	#print temp

	#print shotInd
	
	actual_target_ind = indexToRemove + shotInd

	#print raw_tokens_pass[chosenLineInd][1]
	
	#print len(raw_tokens_pass[chosenLineInd][1])
	#print len(change)

	if check == 0 and len(raw_tokens_pass[chosenLineInd][1]) == len(change):
		before = source_code[:indexToRemove]
	else:
		before = source_code[:actual_target_ind]
	#print "B"
	#print before
	
	
	after = source_code[actual_target_ind+len(raw_tokens_pass[chosenLineInd][1]):]
	#print "A"
	#print after	

	if check == 0:
		#print "GOT EM"
		new_text = before + after[1:]
	else:	
		new_text = before + after

	#print actual_target_ind

	#print '-------------------------------'
	#print new_text
	

	toTest = checkPyPySyntax(new_text)

	if toTest == None:
 		#print "Try again..."	
		#deleteTokMut(raw_tokens_pass, raw_text)
		lenR = 2
		lenK = 2
		return lenR, raw_tokens_pass, raw_text, lenK, send
	else:
		#print toTest[0]
		#print toTest[0].filename
		#print toTest[0].line
		#print toTest[0].column
		#print toTest[0].functionname
		#print toTest[0].text
		#print toTest[0].errorname
		#print "-----------FINISHED-------------------"
		#print chosenLineInd+1
		#print out_tokens_loc
		return new_text, YES_TOKEN, DELETION, out_tokens_loc, send

