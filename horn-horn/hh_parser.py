
"""
@file hh_parser.py
@author André Schrottenloher
@brief A small parser for the Horn-Horn set constraints syntax.

@see hh_lexer.py

The syntax of Horn-Horn set constraints is the following (examples) :

TRUE IMPLIES x2 IN BOTTOM
x4 IN BOTTOM IMPLIES FALSE
x0 INTER x2 IN x4 IMPLIES FALSE
TRUE IMPLIES x4 IN x3

No parentheses are needed nor allowed. A conjunction of set constraints
(inner clauses) implies another constraint.

The parser transforms an outer clause into a 2-tuple (x, l) where x is
an inner clause and l a list of inner clauses ; each inner clause is itself
a 2-tuple (x,l) where x is a literal (set) and l a list of literals.

"""

import ply.yacc as yacc

from hh_lexer import tokens


def p_clause_implies(p):
    'clause : prems IMPLIES term'
    p[0] = (p[3], p[1])

def p_prems_trivial(p):
    'prems : TRUE'
    p[0] = []

def p_prems_term(p):
    'prems : term'
    p[0] = [p[1]]

def p_prems_and(p):
    'prems : prems AND prems'
    p[0] = p[1] + p[3]

def p_term_trivial(p):
    'term : FALSE'
    p[0] = None

def p_top_in_term(p):
    'term : TOP IN ID'
    p[0] = (p[3], [])

def p_term_in_bot(p):
    'term : concept IN BOTTOM'
    p[0] = (None, p[1])

def p_term_in(p):
    'term : concept IN ID'
    p[0] = (p[3], p[1])

def p_concept_inter(p):
    'concept : concept INTER concept'
    p[0] = p[1] + p[3]

def p_concept_id(p):
    'concept : ID'
    p[0] = [p[1]]

# handle syntax errors
def p_error(p):
    if p is not None:
        print("Syntax error in input : %s on line %i, character %i" % (p.__str__(), p.lineno, p.lexpos))

# Builds the parser
HH_PARSER = yacc.yacc()

if __name__ == "__main__":
    print("===========================")
    print("Testing hh_parser.py")
    assert HH_PARSER.parse("TRUE IMPLIES C1 INTER C2 IN BOTTOM") == ((None, ['C1', 'C2']), [])
    assert HH_PARSER.parse("# blabli TRUE blablablanlala") is None
    print("Tests passed.")
