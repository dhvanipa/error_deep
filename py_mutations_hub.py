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

# NUM TOTAL: 462 563
# ACTUAl: 462 561
# ACTUAL: 925 122, BATCH = 66, GOOD = 33, BAD = 33 (I, D, S -> 11)
# Iterations: 14 017
# Unused samples = 2 
# ONE HOT = 87

BATCH_SIZE = 66
EPOCHS = 14017
all_tokens = []
new_tokens = []
indexed_tokens = []
data = None

def one_hot(indexed_tokens):
	one_hot = []
	nb_classes = 87
	one_hot_targets = np.eye(nb_classes)[indexed_tokens]
	one_hot = one_hot_targets.tolist()
	return one_hot
	

def set_from_json(all_tokens):
	print "OMG"
	with open('vocabulary.json') as data_file:    
    		data = json.load(data_file)
		#pprint(data)
	for token in all_tokens:
		toCompare = token.value
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
	
def vocabularize_tokens(all_tokens):
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
    


    all_tokens_iter = all_tokens[:]
    for Token in all_tokens_iter:
        vocab_entry = open_closed_tokens(Token)
	Token.value = vocab_entry
        if Token.type in EXTRANEOUS_TOKENS:
		all_tokens.remove(Token)
   
    for Token in all_tokens:
	print Token.value
    return set_from_json(all_tokens)
 	
	

# Create list of tokens
def handle_token(type, token, (srow, scol), (erow, ecol), line):
    if repr(token)[:2] == 'u\'':
	val = repr(token)[2:len(repr(token))-1]
    else:
        val = repr(token)[1:len(repr(token))-1]
    send = Token(tokenize.tok_name[type], val, srow, scol, erow, ecol, line)
    all_tokens.append(send)
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
	all_rows = c.fetchmany(size=33)
	
	for curr in range(1):
		print all_rows[curr][0]
		print "Got Em..."
		print "Running PyPy test..."
		toTest = checkPyPySyntax(all_rows[curr][0])
		print "DONE"
		print "CURRENT: "
		print curr
		if toTest == None:
			tokenStream = tokenize.tokenize(StringIO.StringIO(all_rows[curr][0]).readline, handle_token)
			print "RAW"			
			print len(all_tokens)
		
			one_hot_good = vocabularize_tokens(all_tokens)
			raw_tokens = tokenize.generate_tokens(StringIO.StringIO(all_rows[curr][0]).readline)		
			source_code = str(all_rows[curr][0])
			
			#MUTATIONS PER TOKEN
			new_text, NO_TOKEN, INSERTION, out_tokens_loc = insertTokMut(raw_tokens, source_code)

			print "NEXT STEP..."
			try:
				newTokenStream = tokenize.tokenize(StringIO.StringIO(new_text).readline, handle_token)
			except tokenize.TokenError:
    				pass
			one_hot_bad = vocabularize_tokens(new_tokens)
			
			#deleteTokMut(raw_tokens, source_code)
			#subTokMut(raw_tokens, source_code)

			# MUTATIONS PER CHARACTER
			# insertMut(source_code)
			#deleteMut(source_code])
			
			#print "LEN"
			#print one_hot_good[0]
			#print one_hot_bad[0]
			
			print len(one_hot_good)
			print len(one_hot_bad)

			one_hot_all = np.concatenate((one_hot_good, one_hot_bad), axis=0)

			#print len(one_hot_all)
			#print one_hot_all[538]

			print "SUCCESS"

	
		else:
			print "Try again..."
	
def perform():
	testTime()

if __name__ == '__main__':
    perform()


