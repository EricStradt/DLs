"""
@file owllexer.py
@author André Schrottenloher
@date April 2016
@brief Lexer for OWL functional syntax.

This lexer recognizes GCIs and RIs expressed in OWL functional syntax. It is
intended to be an interface with an internal EL/EL+ representation.

Currently, the lexer does not recognize the following :
- declarations : Declaration(Class(:AccelerationValue))
- prefixes : Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)
- ontology name : Ontology(<http://www.co-ode.org/ontologies/galen>)

@see owlparser.py

The code of this file is a simple use of PLY which was initially inspired by
this webpage : http://www.dabeaz.com/ply/ply.html#ply_nn23

"""

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
    'SubClassOf',
    'Declaration',
    'Class',
    'ObjectProperty'
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
OWL_LEXER = lex.lex()


if __name__ == "__main__":
    # testing
    OWL_LEXER.input("SubClassOf(:Aminoglycoside :Antimicrobial)")
    # any new call to .input() will cause the lexer to forget the previous...
    # Tokenize
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break      # No more input
    #     print(tok)
        # print(tok.lineno)
