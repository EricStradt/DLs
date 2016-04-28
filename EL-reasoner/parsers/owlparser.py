# ------------------------------------------------------------
# elparser.py
#
# Parser for a small EL / EL+ syntax
# code adapted from http://www.dabeaz.com/ply/ply.html#ply_nn23
# ------------------------------------------------------------

import ply.yacc as yacc

from ellexer import tokens

# ------------------------------------------------------------


# functional are not handled for now
def p_functional(p):
    'expression : FunctionalObjectProperty RPAREN ID LPAREN'
    p[0] = None

def p_transitive(p):
    'expression : TransitiveObjectProperty RPAREN ID LPAREN'
    p[0] = ["RIN", ["RCOMP", p[3], p[3]], p[3]]

def p_equivalent(p):
    'expression : EquivalentClasses RPAREN expression expression LPAREN'
    p[0] = ["EQUIV", p[3], p[4]]

# TODO : check if this is correct in the meaning of sub oject property...
def p_subobjectproperty(p):
    'expression : SubObjectPropertyOf RPAREN expression expression LPAREN'
    p[0] = ["RIN", p[3], p[4]]

def p_objectintersection(p):
    'expression : ObjectIntersectionOf RPAREN expression expression LPAREN'
    p[0] = ["INTER", p[3], p[4]]

def p_objectsomevalues(p):
    'expression : ObjectSomeValuesFrom RPAREN expression expression LPAREN'
    p[0] = ["EXISTS", p[3], p[4]]

def p_subclass(p):
    'expression : SubClassOf RPAREN expression expression LPAREN'
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
EL_PARSER = yacc.yacc()

if __name__ == "__main__":
    result = EL_PARSER.parse('SubObjectPropertyOf(:ChemicalProcessModifierAttribute :ProcessModifierAttribute)\n')
    print(result)
