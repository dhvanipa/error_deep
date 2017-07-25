# Copyright 2017 Dhvani Patel

import cv2
from check_pypy_syntax import checkPyPySyntax
from compile_error import CompileError
import sqlite3
import tokenize
import token
import StringIO
import keyword
from Token import Token
import json

global all_tokens

def one_hot(indexed_tokens):
	one_hot = []
	nb_classes = 88
	one_hot_targets = np.eye(nb_classes)[indexed_tokens]
	one_hot = one_hot_targets.tolist()
	#print "fort"
	#bruhTemp = one_hot[:]
	for x in range(len(one_hot)):
		#one_hot[x].astype(int)
		[int(i) for i in one_hot[x]]
	#one_hot.astype(int)
	#print type(one_hot[0][0])
	return one_hot
	

def set_from_json(all_tokens, flag):
	#print "OMG"
	with open('vocabulary.json') as data_file:    
    		data = json.load(data_file)
		#pprint(data)

	tempT = all_tokens[:]
	for token in tempT:
		if len(token.value) > 0:
			if token.value[0] == '#':
				all_tokens.remove(token)
				#print "no way"

	for token in all_tokens:
		if token.value == "\\r\\n":
			token.value = "NEWLINE"
		toCompare = token.value
		#print token.type
		#print "Broke..."
		#print token.line
		global indexed_tokens
		indexed_tokens.append(data["indexes"].index(toCompare))
	for r in range(9):
		indexed_tokens.insert(r, data["indexes"].index(START_TOKEN))
		indexed_tokens.append(data["indexes"].index(END_TOKEN))
		
	#print indexed_tokens
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
   
    #for Token in every_token:
    #print Token.value
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

def create(numFile):

	sqlite_file = "/home/dhvani/python-sources.sqlite3"
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()
	#print "Success Connection to database..."
	c.execute("SELECT source FROM source_file INNER JOIN eligible_source ON source_file.hash = eligible_source.hash")
	#print "Executed SELECT..."
	#print "Fetching all rows..."
	all_rows = c.fetchmany(size=2100)
	conn.close()
	toTest = checkPyPySyntax(all_rows[numFile][0])
		
	if toTest == None:
		#print all_rows[numFile][0]
		global all_tokens
		all_tokens = []
		tokenStream = tokenize.tokenize(StringIO.StringIO(all_rows[numFile][0]).readline, handle_token)
		allGood = all_tokens[:]
		one_hot_good = vocabularize_tokens(all_tokens, False)
#		print one_hot_good

	else:
		print "Try again..."
		print numFile


if __name__ == '__main__':
    create(2)
