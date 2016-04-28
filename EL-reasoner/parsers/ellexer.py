"""
@file ellexer.py
@author André Schrottenloher
@date April 2016
@brief Lexer for a small EL / EL+ syntax.

This lexer accepts a small EL / EL+ syntax.
It uses PLY.

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
