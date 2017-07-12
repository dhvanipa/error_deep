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

# NUM TOTAL: 462 563
# / 3 = 154 187
# ONE HOT = 87

all_tokens = []
indexed_tokens = []
one_hot = []
data = None

def one_hot(indexed_tokens):
	nb_classes = 87
	one_hot_targets = np.eye(nb_classes)[indexed_tokens]
	one_hot = one_hot_targets.tolist()
	print one_hot[15]
	

def set_from_json(all_tokens):
	print "OMG"
	with open('vocabulary.json') as data_file:    
    		data = json.load(data_file)
		#pprint(data)
	for token in all_tokens:
		toCompare = token.value
		indexed_tokens.append(data["indexes"].index(toCompare))
	print indexed_tokens
	one_hot(indexed_tokens)

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
	#print Token.type
        vocab_entry = open_closed_tokens(Token)
        #print vocab_entry
	Token.value = vocab_entry
        if Token.type in EXTRANEOUS_TOKENS:
		all_tokens.remove(Token)
   
    for Token in all_tokens:
	print Token.value
    set_from_json(all_tokens)
 	
	

# Create list of tokens
def handle_token(type, token, (srow, scol), (erow, ecol), line):
    send = Token(tokenize.tok_name[type], repr(token)[1:len(repr(token))-1], srow, scol, erow, ecol, line)
    #print send
    all_tokens.append(send)
    #print type.exact_type
    
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
	toTest = checkPyPySyntax(all_rows[0])
	print "DONE"
	if toTest == None:
		#output = ''
		#print output
		tokenStream = tokenize.tokenize(StringIO.StringIO(all_rows[0]).readline, handle_token)
		#print all_tokens		
		vocabularize_tokens(all_tokens)
		raw_tokens = tokenize.generate_tokens(StringIO.StringIO(all_rows[0]).readline)		
		raw_tokens_pass = []
		
# TO DO: REMOVE COMMENTS FROM SOURCE FOR MUTATIONS				
#		for token in raw_tokens:
#			print token
#			if token[0] != 53:
#				raw_tokens_pass.append(list(token))
#		source_code = tokenize.untokenize(raw_tokens_pass)

		insertMut(all_rows[0])
		print "SUCCESS"
	else:
		print "Try again..."

if __name__ == '__main__':
    testTime()


