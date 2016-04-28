"""
@file ellexer.py
@author André Schrottenloher
@date April 2016
@brief Lexer for a small EL / EL+ syntax.

This lexer accepts a small EL / EL+ syntax.

It recognizes the following reserved words :
- IN : concept inclusion
- INTER : concept intersection
- EXISTS : existential restriction
- RIN : role inclusion
- RCOMP : role composition
- EQUIV : concept equivalence
- TOP : Entire domain
- BOTTOM : Empty set
- NOT : negation

All other words can be used as concept or role names.
The special character "#" can be used for comments.

The code of this file is a simple use of PLY which was initially inspired by
this webpage : http://www.dabeaz.com/ply/ply.html#ply_nn23

@see elparser.py

"""

import ply.lex as lex

tokens = [
   'ID',
   'RPAREN',
   'LPAREN',
   'VIRG'
]

reserved = [
   'IN',
   'INTER',
   'EXISTS',
   'RIN',
   'RCOMP',
   'EQUIV',
   'TOP',
   'BOTTOM',
   'NOT'
]

tokens = tokens + reserved

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_VIRG = r','

def t_COMMENT(t):
    r'\#.*'
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = t.value
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# handles end of file
def t_eof(t):
    return None

# Build the lexer
lexer = lex.lex()

if __name__ == "__main__":
    # TODO add proper tests
    # testing
    lexer.input("((EXISTS r (EXISTS s C1)) INTER C2) IN C5")
    # any new call to .input() will cause the lexer to forget the previous...
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
        # print(tok.lineno)
