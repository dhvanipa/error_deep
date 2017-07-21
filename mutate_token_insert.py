# Copyright 2017 Dhvani Patel

import json
from pprint import pprint
import tokenize
from check_pypy_syntax import checkPyPySyntax
from compile_error import CompileError
import token
from Token import Token
from random import randint
import StringIO


#Declaring Global Constants
YES_TOKEN = 0b10
NO_TOKEN = 0b01
INSERTION = 0b001
DELETION = 0b010
SUBSTITUTION = 0b100

global new_token

# Method for finding index of certain characters in a string, n being the n'th occurence of the character/string
def find_nth(haystack, needle, n):
    start = haystack.find(needle.encode())
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# Create list of tokens
def handle_token(type, token, (srow, scol), (erow, ecol), line):
    if repr(token)[:2] == 'u\'':
	val = repr(token)[2:len(repr(token))-1]
    else:
        val = repr(token)[1:len(repr(token))-1]
    send = Token(tokenize.tok_name[type], val, srow, scol, erow, ecol, line)
    global new_token
    new_token.append(send)
    #print "%d,%d-%d,%d:\t%s\t%s" % \
    #    (srow, scol, erow, ecol, tokenize.tok_name[type], repr(token))

def insertTokMutS(raw_tokens, all_tokens, raw_text):
	new_text = raw_text
	with open('vocabulary_mutate.json') as data_file:    
    		data = json.load(data_file)
		#pprint(data)
		#print "HI"
	#print len(data["indexes_m"])
	
	#print chosenToken

	#print tokenize.tok_name
	
	#insTok = Token(
	
	out_tokens_loc = []
	raw_tokens_pass = []
	actual_token_len = []
	orig = []
	for token in all_tokens:
		token_use = token		
		#orig.append(token_use)
		actual_token_len.append(token_use)

	for token in raw_tokens:
		token_use = token		
		orig.append(token_use)
	
		raw_tokens_pass.append(token_use)
					
	#from py_mutations_hub import getRid
	#print "OKAY"
	#print len(raw_tokens_pass)
	#test = getRid(raw_tokens_pass, True)
	#print len(test)
	#print len(actual_token_len)
	#print type(radha)
	
	num_lines = len(actual_token_len)
	num_encode = len(orig)	
	if (num_lines % 10 == 0):
		numTokensNeeded = int((num_lines / 10))
	else:
		numTokensNeeded = int((num_lines / 10))
	insToks = []
	chosens = []

	#print numTokensNeeded
	#print "import num"
	haha = -1
	radOut = 0
	while radOut < numTokensNeeded:
		#chosen = raw_tokens_pass[chosenLineInd]

		chosenInd = randint(0,84)
		chosenToken = data["indexes_m"][chosenInd]
		#print "RAD S"
		#print radOut
		#print len(chosens)
		#print len(insToks)
		#print "RAD O"

		global new_token
		new_token = []
		try:
			toksG = tokenize.tokenize(StringIO.StringIO(chosenToken).readline, handle_token)
		except tokenize.TokenError:
			pass	
		#print type(toksG)
		#print len(new_token)
		insEdTok = new_token[0]
		insTok = insEdTok
		insToks.append(insTok)
		#print num_lines
		if radOut == (numTokensNeeded-1):
			param_start = haha
			param_end = num_lines-1
		else:
			param_start = radOut * 10
			param_end = param_start + 9
			haha = param_end
		chosenLineInd = randint(param_start, param_end) #num_lines-1
		#print "inds"
		#print chosenLineInd
		#print "stop"
		#chosen = raw_tokens_pass[chosenLineInd]
		chosen = actual_token_len[chosenLineInd]
		#chosen = Token(tokenize.tok_name[raw_tokens_pass[chosenLineInd][0]], raw_tokens_pass[chosenLineInd][1], raw_tokens_pass[chosenLineInd][2][0], raw_tokens_pass[chosenLineInd][2][1], raw_tokens_pass[chosenLineInd][3][0], raw_tokens_pass[chosenLineInd][3][1], raw_tokens_pass[chosenLineInd][4])
		chosens.append(chosen)

		source_code = raw_text

		#print len(source_code)

		#print raw_tokens_pass[chosenLineInd][0]

		#print all_tokens[chosenLineInd].value
		#print num_lines - 1
		#print len(raw_tokens_pass)
		#print len(actual_token_len)
		#print raw_tokens_pass[50][4]
		#print actual_token_len[chosenLineInd].line
		#print raw_text
		toAddBeforeInd = source_code.index(actual_token_len[chosenLineInd].line)
		#print toAddBeforeInd
	
		temp = source_code[toAddBeforeInd:toAddBeforeInd+len(actual_token_len[chosenLineInd].line)]
		#print temp
		#print actual_token_len[chosenLineInd].value
		#print "kobe"
		#print raw_tokens_pass[chosenLineInd][1]

		shotInd = temp.index(raw_tokens_pass[chosenLineInd][1])

		change = temp.strip()
		check = temp.index(change)	
		#print check

		#print len(temp)
		#print shotInd

		if shotInd+1 == len(temp):
			shotInd = shotInd-1

		actual_target_ind = toAddBeforeInd + shotInd


		before = source_code[:actual_target_ind+len(raw_tokens_pass[chosenLineInd][1])]
		#print "B"
		#print before
		
		after = source_code[actual_target_ind+len(raw_tokens_pass[chosenLineInd][1]):]
		#print "A"
		#print after	
		#print raw_tokens_pass[chosenLineInd][0]

		if raw_tokens_pass[chosenLineInd][0] == 53:
			chosenToken = '\n' + chosenToken

		if shotInd == 0:
			if raw_tokens_pass[chosenLineInd][0] == 4:
				new_text = before + chosenToken.encode() + after
			else:
				new_text = before + ' ' + chosenToken.encode() + ' ' + after
		else:
			if raw_tokens_pass[chosenLineInd][0] == 54:
				new_text = before + chosenToken.encode() + after
		
			elif chosenInd == data["indexes_m"].index('\n'): 
				#print "shiz"
				if after[0] == ' ':
					space = ' ' * (check-1)
				else:
					space = ' ' * (check)
				new_text = before + chosenToken.encode() + space + after
			else:
				new_text = before + ' ' + chosenToken.encode() + ' ' + after
		toTest = checkPyPySyntax(new_text)
		if toTest == None:
			#print radOut
			#if radOut != 0:
			#	radOut = radOut-1
			#else:
			#	radOut = 0
			#print radOut	
			radOut = radOut
			insToks.remove(insTok)
			chosens.remove(chosen)
			#print "test_t"
		else:
			radOut = radOut + 1

		'''
		print "Overthink"
		print len(orig)
		print numTokensNeeded
		print len(insToks)
		print insToks[0].value
		print len(chosens)
		print chosens[0].value
		print "relax"
		'''
		#print NAH
		#print "NAH"
	#print ".___."	
	#print len(chosens)
	#print len(insToks)
	#print "NAH"

	return new_text, NO_TOKEN, INSERTION, out_tokens_loc, chosens, insToks
	
	#print "-----------FINISHED-------------------"
	#print chosenLineInd+1	
	#print out_tokens_loc
	#print len(raw_tokens_pass)
	#print len(out_tokens_loc)
	#print lenD
	#print chosenTrueLineInd




def insertTokMut(raw_tokens, raw_text):

	with open('vocabulary_mutate.json') as data_file:    
    		data = json.load(data_file)
		#pprint(data)
		#print "HI"
	#print len(data["indexes_m"])
	
	#print chosenToken

	#print tokenize.tok_name
	
	#insTok = Token(
	
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
						#print token

	#print "OKAY"
	
	
	
	num_lines = len(raw_tokens_pass)
	num_encode = len(orig)	

	numTokensNeeded = int((num_lines / 10)) + 1
	insToks = []
	chosens = []

	#print numTokensNeeded
	#print "import num"
	for rad in range(numTokensNeeded):
		
		#chosen = raw_tokens_pass[chosenLineInd]

		chosenInd = randint(0,84)
		chosenToken = data["indexes_m"][chosenInd]

		global new_token
		new_token = []
		try:
			toksG = tokenize.tokenize(StringIO.StringIO(chosenToken).readline, handle_token)
		except tokenize.TokenError:
			pass	
		#print type(toksG)
		#print len(new_token)
		insEdTok = new_token[0]
		insTok = insEdTok
		insToks.append(insTok)
		#print num_lines
		if rad == (numTokensNeeded-1):
			param_start = param_end
			param_end = num_lines-1
		else:
			param_start = rad * 10
			param_end = param_start + 9
		
		chosenLineInd = randint(param_start, param_end) #num_lines-1
		#print "inds"
		#print chosenLineInd
		#print "stop"
		chosen = Token(tokenize.tok_name[raw_tokens_pass[chosenLineInd][0]], raw_tokens_pass[chosenLineInd][1], raw_tokens_pass[chosenLineInd][2][0], raw_tokens_pass[chosenLineInd][2][1], raw_tokens_pass[chosenLineInd][3][0], raw_tokens_pass[chosenLineInd][3][1], raw_tokens_pass[chosenLineInd][4])
		chosens.append(chosen)

		'''
		print "Overthink"
		print len(orig)
		print numTokensNeeded
		print len(insToks)
		print insToks[0].value
		print len(chosens)
		print chosens[0].value
		print "relax"
		'''
		#print NAH
		#print "NAH"

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
			if indI == indLook+1:
				out_tokens_loc[indI] = ('1')

		source_code = raw_text

		#print len(source_code)

		#print raw_tokens_pass[chosenLineInd][0]

	
		#print raw_tokens_pass[chosenLineInd][4]
		#print raw_text
		toAddBeforeInd = source_code.index(raw_tokens_pass[chosenLineInd][4])

	
		temp = source_code[toAddBeforeInd:toAddBeforeInd+len(raw_tokens_pass[chosenLineInd][4])]
		#print temp
		#print "kobe"
		#print raw_tokens_pass[chosenLineInd][1]

		shotInd = temp.index(raw_tokens_pass[chosenLineInd][1])

		change = temp.strip()
		check = temp.index(change)	
		#print check

		#print len(temp)
		#print shotInd

		if shotInd+1 == len(temp):
			shotInd = shotInd-1

		actual_target_ind = toAddBeforeInd + shotInd


		before = source_code[:actual_target_ind+len(raw_tokens_pass[chosenLineInd][1])]
		#print "B"
		#print before
		
		after = source_code[actual_target_ind+len(raw_tokens_pass[chosenLineInd][1]):]
		#print "A"
		#print after	
		#print raw_tokens_pass[chosenLineInd][0]

		if shotInd == 0:
			if raw_tokens_pass[chosenLineInd][0] == 4:
				new_text = before + chosenToken.encode() + after
			else:
				new_text = before + ' ' + chosenToken.encode() + ' ' + after
		else:
			if raw_tokens_pass[chosenLineInd][0] == 54:
				new_text = before + chosenToken.encode() + after
		
			elif chosenInd == data["indexes_m"].index('\n'): 
				#print "shiz"
				if after[0] == ' ':
					space = ' ' * (check-1)
				else:
					space = ' ' * (check)
				new_text = before + chosenToken.encode() + space + after
			else:
				new_text = before + ' ' + chosenToken.encode() + ' ' + after
		toTest = checkPyPySyntax(new_text)
		if toTest == None:
			print rad
			rad = rad-1
			print rad	
			insToks.remove(insTok)
			chosens.remove(chosen)
			print "test_t"
	#print '------------------------------------'
	#print new_text

	toTest = checkPyPySyntax(new_text)

	if toTest == None:
 		#print "Try again..."	
		#print "-----------FINISHED-------------------"
		#insertTokMut(raw_tokens_pass, raw_text)
		#print "-----------FINISHED-------------------"
		#print "shit man"
		lenR = 2
		lenK = 2
		return lenR, raw_tokens_pass, raw_text, actual_token_len, chosens, insToks
	else:
		#print "-----------FINISHED-------------------"
		#print toTest[0]
		#print toTest[0].filename
		#print toTest[0].line
		#print toTest[0].column
		#print toTest[0].functionname
		#print toTest[0].text
		#print toTest[0].errorname
		#print type(out_tokens_loc)
		#print len(new_text)
		#print NO_TOKEN
		#print INSERTION
		#print len(out_tokens_loc)
		return new_text, NO_TOKEN, INSERTION, out_tokens_loc, chosens, insToks
	
	#print "-----------FINISHED-------------------"
	#print chosenLineInd+1	
	#print out_tokens_loc
	#print len(raw_tokens_pass)
	#print len(out_tokens_loc)
	#print lenD
	#print chosenTrueLineInd

