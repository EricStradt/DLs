"""
@file owlparser.py
@author André Schrottenloher
@date April 2016
@brief Parser for OWL functional syntax.

This parser recognizes EL/EL+ GCIs and RIs only. As a consequence, it only
handles a subset of the language recognized by the lexer in file owllexer.py,
for example, no functionality or number restrictions on roles are allowed.


The code of this file is a simple use of PLY which was initially inspired by
this webpage : http://www.dabeaz.com/ply/ply.html#ply_nn23

@see owllexer.py

"""

import ply.yacc as yacc

try:
    from owllexer import tokens, OWL_LEXER
except ImportError as e:
    from parsers.owl.owllexer import tokens, OWL_LEXER


def reverse_parser(line):
    # TODO
    raise NotImplementedError("Fail")

def p_declaration(p):
    'expression : Declaration LPAREN expression RPAREN'
    p[0] = None

def p_class(p):
    'expression : Class LPAREN ID RPAREN'
    p[0] = None

def p_objectprop(p):
    'expression : ObjectProperty LPAREN ID RPAREN'
    p[0] = None

# functional are not handled for now
def p_functional(p):
    'expression : FunctionalObjectProperty LPAREN ID RPAREN'
    p[0] = None

def p_transitive(p):
    'expression : TransitiveObjectProperty LPAREN ID RPAREN'
    p[0] = ["RIN", ["RCOMP", p[3], p[3]], p[3]]

def p_equivalent(p):
    'expression : EquivalentClasses LPAREN expression expression RPAREN'
    p[0] = ["EQUIV", p[3], p[4]]

# TODO : check if this is correct in the meaning of sub oject property...
def p_subobjectproperty(p):
    'expression : SubObjectPropertyOf LPAREN expression expression RPAREN'
    p[0] = ["RIN", p[3], p[4]]

def p_objectintersection(p):
    'expression : ObjectIntersectionOf LPAREN expression expression RPAREN'
    p[0] = ["INTER", p[3], p[4]]

def p_objectsomevalues(p):
    'expression : ObjectSomeValuesFrom LPAREN expression expression RPAREN'
    p[0] = ["EXISTS", p[3], p[4]]

def p_subclass(p):
    'expression : SubClassOf LPAREN expression expression RPAREN'
    p[0] = ["IN", p[3], p[4]]

def p_id(p):
    'expression : ID'
    p[0] = p[1]


def p_error(p):
    if p is not None:
        print("Syntax error in input : %s on line %i, character %i" % (p.__str__(), p.lineno, p.lexpos))
    else:
        print("Syntax error")

# Build the parser
OWL_PARSER = yacc.yacc()

if __name__ == "__main__":

    tests = [
        "SubObjectPropertyOf(:ChemicalProcessModifierAttribute :ProcessModifierAttribute)\n",
        "SubClassOf(:Abdomen ObjectSomeValuesFrom(:hasShapeAnalagousTo ObjectIntersectionOf(:AnatomicalShape ObjectSomeValuesFrom(:hasState :laminar))))",
        "SubClassOf(ObjectIntersectionOf(:AcuteMyocardialInfarction ObjectSomeValuesFrom(:hasSublocation :OtherLateralWall)) ObjectSomeValuesFrom(:isPairedOrUnpaired :exactlyPaired))"
    ]

    # TODO : add proper tests
    for t in tests:
        print(OWL_PARSER.parse(t, lexer=OWL_LEXER))
    # result = OWL_PARSER.parse('')
    # print(result)
    # result = OWL_par
