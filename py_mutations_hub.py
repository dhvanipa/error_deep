# Copyright 2017 Dhvani Patel

import sqlite3
from check_pypy_syntax import checkPyPySyntax
from compile_error import CompileError
import tokenize
import token
import StringIO
import keyword
from Token import Token
import json
#from pprint import pprint
import numpy as np
from mutate_insert import insertMut
from mutate_deletion import deleteMut
from mutate_token_insert import insertTokMut
from mutate_token_delete import deleteTokMut
from mutate_token_sub import subTokMut
import sys

# NUM TOTAL: 462 563
# ACTUAl: 462 540
# ACTUAL: 925 080, BATCH = 60, GOOD = 30, BAD = 30 (I, D, S -> 10)
# Iterations: 15 418
# Unused samples = 23 
# ONE HOT = 87
# OUT = 104 (2 + 2 + 3 + 10 + 87)
# 10 = WINDOW SIZE

BATCH_SIZE = 66
NUM_BITS_OUTPUT = 104
global all_tokens
new_tokens_ins = []
new_tokens_del = []
new_tokens_sub = []
global indexed_tokens
data = None

#Declaring Global Constants
YES_TOKEN = 0b00
NO_TOKEN = 0b01
INSERTION = 0b001
DELETION = 0b010
SUBSTITUTION = 0b100
YES_ERROR = 0b00
NO_ERROR = 0b01

START_TOKEN = '<s>'
END_TOKEN = '</s>'

def one_hot(indexed_tokens):
	one_hot = []
	nb_classes = 87
	one_hot_targets = np.eye(nb_classes)[indexed_tokens]
	one_hot = one_hot_targets.tolist()
	return one_hot
	

def set_from_json(all_tokens, flag):
	print "OMG"
	with open('vocabulary.json') as data_file:    
    		data = json.load(data_file)
		#pprint(data)
	for token in all_tokens:
		toCompare = token.value
		print token.type
		#print "Broke..."
		#print token.line
		global indexed_tokens
		indexed_tokens.append(data["indexes"].index(toCompare))
	print indexed_tokens
	return one_hot(indexed_tokens)

def open_closed_tokens(token):
    """
    'Flattens' Python into tokens based on whether the token is open or
    closed.
    """

    # List of token names that whose text should be used verbatim as the type.
    VERBATIM_CLASSES = {
        "AMPER", "AMPEREQUAL", "ASYNC", "AT", "ATEQUAL", "AWAIT", "CIRCUMFLEX",
        "CIRCUMFLEXEQUAL", "COLON", "COMMA", "DOT", "DOUBLESLASH",
        "DOUBLESLASHEQUAL", "DOUBLESTAR", "DOUBLESTAREQUAL", "ELLIPSIS",
        "EQEQUAL", "EQUAL", "GREATER", "GREATEREQUAL", "LBRACE", "LEFTSHIFT",
        "LEFTSHIFTEQUAL", "LESS", "LESSEQUAL", "LPAR", "LSQB", "MINEQUAL",
        "MINUS", "NOTEQUAL", "OP", "PERCENT", "PERCENTEQUAL", "PLUS", "PLUSEQUAL",
        "RARROW", "RBRACE", "RIGHTSHIFT", "RIGHTSHIFTEQUAL", "RPAR", "RSQB",
        "SEMI", "SLASH", "SLASHEQUAL", "STAR", "STAREQUAL", "TILDE", "VBAR",
        "VBAREQUAL"
    }
 
    OTHER = { "NEWLINE", "INDENT", "DEDENT"}
    CHECK = {"None", "True", "False"}

    if token.type == 'NAME':
        # Special case for NAMES, because they can also be keywords.
        if keyword.iskeyword(token.value):
            return token.value
	elif token.value in CHECK:
	    return token.value
        else:
            return '<IDENTIFIER>'
    elif token.type in VERBATIM_CLASSES:
        # These tokens should be mapped verbatim to their names.
        assert ' ' not in token.value
        return token.value
    elif token.type in {'NUMBER', 'STRING'}:
        # These tokens should be abstracted.
        # Use the <ANGLE-BRACKET> notation to signify these classes.        
	return "<" + token.type.upper() + ">"
    elif token.type in OTHER:
        return token.type
    else:
        # Use these token's name verbatim.
       # assert token.type in {
        #    'NEWLINE', 'INDENT', 'DEDENT',
        #    'ENDMARKER', 'ENCODING', 'COMMENT', 'NL', 'ERRORTOKEN'
        #}
	
        return token.value
	
def vocabularize_tokens(every_token, flag):
    if flag == False:
   	 EXTRANEOUS_TOKENS = {
             # Always occurs as the first token: internally indicates the file
             # ecoding, but is irrelelvant once the stream is already tokenized
            'ENCODING',
	
            # Always occurs as the last token.
            'ENDMARKER',

            # Insignificant newline; not to be confused with NEWLINE
            'NL',
	
            # Discard comments
            'COMMENT',

            # Represents a tokenization error. This should never appear for
            # syntatically correct files.
            'ERRORTOKEN',
        }
    elif flag == True:
        EXTRANEOUS_TOKENS = {
             # Always occurs as the first token: internally indicates the file
             # ecoding, but is irrelelvant once the stream is already tokenized
            'ENCODING',
	
            # Always occurs as the last token.
            'ENDMARKER',

            # Discard comments
            'COMMENT',

            # Represents a tokenization error. This should never appear for
            # syntatically correct files.
            'ERRORTOKEN',
        }
    


    all_tokens_iter = every_token[:]
    for Token in all_tokens_iter:
        vocab_entry = open_closed_tokens(Token)
	Token.value = vocab_entry
        if Token.type in EXTRANEOUS_TOKENS:
		every_token.remove(Token)
	if flag == True:
		if Token.value == "\\n":
			every_token.remove(Token)
		if Token.type == "NL":
			print "Gotch u"
   
    for Token in every_token:
	print Token.value
    return set_from_json(every_token, flag)
 	
	

# Create list of tokens
def handle_token(type, token, (srow, scol), (erow, ecol), line):
    if repr(token)[:2] == 'u\'':
	val = repr(token)[2:len(repr(token))-1]
    else:
        val = repr(token)[1:len(repr(token))-1]
    send = Token(tokenize.tok_name[type], val, srow, scol, erow, ecol, line)
    global all_tokens
    all_tokens.append(send)
    print "%d,%d-%d,%d:\t%s\t%s" % \
        (srow, scol, erow, ecol, tokenize.tok_name[type], repr(token))


def perform():
	sqlite_file = "/home/dhvani/python-sources.sqlite3"
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()
	print "Success Connection to database..."
	c.execute("SELECT source FROM source_file INNER JOIN eligible_source ON source_file.hash = eligible_source.hash")
	print "Executed SELECT..."
	print "Fetching all rows..."
	all_rows = c.fetchmany(size=33)
	
	for curr in range(1):
		curr = 2
		print all_rows[curr][0]
		print "Got Em..."
		print "Running PyPy test..."
		toTest = checkPyPySyntax(all_rows[curr][0])
		print "DONE"
		print "CURRENT: "
		print curr
		if toTest == None:
			global all_tokens
			all_tokens = []
			global indexed_tokens
			indexed_tokens = []
			tokenStream = tokenize.tokenize(StringIO.StringIO(all_rows[curr][0]).readline, handle_token)
			print "RAW"		
			print len(all_tokens)
			allGood = all_tokens[:]
			one_hot_good = vocabularize_tokens(all_tokens, False)
			one_hot_gOut = [0] * NUM_BITS_OUTPUT

			print "DHVANI"
			print len(one_hot_good)
			print len(allGood)
		
			raw_tokens = tokenize.generate_tokens(StringIO.StringIO(all_rows[curr][0]).readline)		
			source_code = str(all_rows[curr][0])
			
			#MUTATIONS PER TOKEN

			# INSERT
			#global all_tokens
			#all_tokens = []
			global indexed_tokens
			indexed_tokens = []
			print "RAW"		
			print len(all_tokens)
			
			new_i_text, NO_TOKEN, INSERTION, out_tokens_loc, chosenTrueLineInd, insTok = insertTokMut(raw_tokens, source_code)

			while isinstance(new_i_text, int):
				new_i_text, NO_TOKEN, INSERTION, out_tokens_loc, chosenTrueLineInd, insTok = insertTokMut(NO_TOKEN, INSERTION)
				if isinstance(new_i_text, str):
					break
					
			new_tokens_ins = all_tokens
	
			if insTok.type == "NL":
				insTok.type = "NEWLINE"

			vocab_entry = open_closed_tokens(chosenTrueLineInd)
			chosenTrueLineInd.value = vocab_entry
			print vocab_entry

			bruhInd = -1
			iterInd = 0
			for a in allGood:
				if a == chosenTrueLineInd:
					bruhInd = iterInd
				iterInd = iterInd + 1
			print bruhInd + 1
			new_tokens_ins.insert(bruhInd+1, insTok)
		
			print "NEXT STEP...C"

			one_hot_bad_ins = vocabularize_tokens(new_tokens_ins, True)
			

			# DELETE
			raw_tokens = tokenize.generate_tokens(StringIO.StringIO(all_rows[curr][0]).readline)	
			#global all_tokens
			#all_tokens = []
			global indexed_tokens
			indexed_tokens = []
			print type(raw_tokens)
			print type(source_code)
			new_d_text, YES_TOKEN, DELETION, out_tokens_loc_d, send = deleteTokMut(raw_tokens, source_code)

			while isinstance(new_d_text, int):
				new_d_text, YES_TOKEN, DELETION, out_tokens_loc, send = deleteTokMut(YES_TOKEN, DELETION)
				if isinstance(new_d_text, str):
					break
			

			print "NEXT STEP..."
			
			new_tokens_del = allGood

			vocab_entry = open_closed_tokens(send)
			send.value = vocab_entry
			
			bruhInd = -1
			iterInd = 0
			for a in allGood:
				if a == send:
					bruhInd = iterInd
				iterInd = iterInd + 1
			print bruhInd
			print len(new_tokens_del)
			del new_tokens_del[bruhInd]		
			print len(new_tokens_del)
			print "DEL ROR"

			one_hot_bad_del = vocabularize_tokens(new_tokens_del, True)

		
			# SUB
			raw_tokens = tokenize.generate_tokens(StringIO.StringIO(all_rows[curr][0]).readline)	
			global all_tokens
			all_tokens = []
			global indexed_tokens
			indexed_tokens = []
			print type(raw_tokens)
			
			new_s_text, YES_TOKEN, SUBSTITUTION, out_tokens_loc_s, sendS = subTokMut(raw_tokens, source_code)

			print "NEXT STEP..."
			try:
				newTokenStream = tokenize.tokenize(StringIO.StringIO(new_s_text).readline, handle_token)
			except (tokenize.TokenError) as e:
    				pass	
			new_tokens_sub = all_tokens
			one_hot_bad_sub = vocabularize_tokens(new_tokens_sub, True)

			# MUTATIONS PER CHARACTER
			# insertMut(source_code)
			#deleteMut(source_code])
			
			#print "LEN"
			#print one_hot_good[0]
			#print one_hot_bad[0]
			
			print len(one_hot_good)
			print len(one_hot_bad_ins)
			print len(one_hot_bad_del)
			print len(one_hot_bad_sub)
			print source_code
			print len(new_i_text)
			print len(new_d_text)
			print new_i_text

			print len(new_tokens_del)
			print len(allGood)
		

			if len(one_hot_bad_del) != len(one_hot_good)-1:
				for token in new_tokens_ins:
					#print token.type
					print token.value
				print "<3 <3 <3 GOOD:"
				for token in allGood:
					#print token.type
					print token.value
			else:
				perform()
				return
				
			#one_hot_all = np.concatenate((one_hot_good, one_hot_bad), axis=0)

			print "SUCCESS"
			ok = one_hot_good, one_hot_bad_ins, one_hot_bad_del, one_hot_bad_sub
			
		else:
			print "Try again..."
	

if __name__ == '__main__':
    perform()


