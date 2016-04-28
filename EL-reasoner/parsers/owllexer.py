# ------------------------------------------------------------
# ellexer.py
#
# Lexer for a small EL / EL+ syntax
# code adapted from http://www.dabeaz.com/ply/ply.html#ply_nn23
# ------------------------------------------------------------
import ply.lex as lex

tokens = [
   'ID',
   'RPAREN',
   'LPAREN',
]

reserved = [
    'SubObjectPropertyOf',
    'EquivalentClasses',
    'ObjectIntersectionOf',
    'ObjectSomeValuesFrom',
    'FunctionalObjectProperty',
    'TransitiveObjectProperty',
    'SubClassOf'
]

tokens = tokens + reserved

t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_COMMENT(t):
    r'\#.*'
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = t.value
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    if t.value[0] == ":":
        t.lexer.skip(1)
    else:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


# handles end of file
def t_eof(t):
    return None

# Build the lexer
lexer = lex.lex()


if __name__ == "__main__":
    # testing
    lexer.input("SubClassOf(:Aminoglycoside :Antimicrobial)")
    # any new call to .input() will cause the lexer to forget the previous...
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
        # print(tok.lineno)
