"""
@file hh_lexer.py
@author André Schrottenloher
@brief Lexer for a small Horn-Horn set constraints syntax.

This file is a lexer for the syntax of Horn-Horn set constraints. It uses ply,
which uses lex / yacc.

The lexer recognizes the following reserved words for inner clauses (set inclusions) :
- IN
- INTER
- BOTTOM
- TOP
It recognizes the following for outer clauses (Horn clauses where the terms are
set inclusions as before) :
- AND
- IMPLIES
- TRUE
- FALSE

All other words can be used as set names.

The special character "#" can be used for comments.

@see hh_parser.py

"""

try:
    import ply.lex as lex
except ImportError as e:
    print("WARNING : The PLY module seems not to be installed. Some features may not work correctly.")


tokens = [
   'ID',
]

reserved = {
    'IN' : 'IN',
    'INTER' : 'INTER',
    'AND' : 'AND',
    'IMPLIES' : 'IMPLIES',
    'BOTTOM' : 'BOTTOM',
    'FALSE' : 'FALSE',
    'TRUE' : 'TRUE',
    'TOP' : 'TOP'
}


tokens = tokens + list(set(reserved.values()))

# rule to dismiss comments
def t_COMMENT(t):
    r'\#.*'
    pass

# rule for the 'ID' token (in fact, any token)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# this rule allows us to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ignored characters
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# handles end of file
def t_eof(t):
    return None

# Builds the lexer
lexer = lex.lex()

if __name__ == "__main__":
    print("============================")
    print("Testing file hh_lexer.py")
    print("Inputting : C2 IN C1 IMPBLIES C4 IN C5")
    lexer.input("C2 IN C1 IMPBLIES C4 IN C5")

    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
