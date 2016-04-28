"""
@file elparser.py
@author André Schrottenloher
@date April 2016
@brief Parser for a small EL / EL+ syntax.

This parser accepts a small EL / EL+ syntax. It parses it to an internal
representation using tree-like nested python objects (lists).

Examples :

Usage :
@code
    from elparser import EL_PARSER
    parsed = EL_PARSER.parse('MentalProcess INTER EXISTS hasIntrinsicAbnormalityStatus nonNormal IN ZC2925\n')
    print(parsed)
@endcode

The code of this file is a simple use of PLY which was initially inspired by
this webpage : http://www.dabeaz.com/ply/ply.html#ply_nn23

@see ellexer.py

"""

import ply.yacc as yacc

try:
    from ellexer import tokens, EL_LEXER
except ImportError as e:
    from parsers.el.ellexer import tokens, EL_LEXER


def reverse_parser(l):
    """
    Reverses the parser.
    """
    if type(l) == str:
        return l
    elif type(l) == list:
        if l[0] == "EXISTS":
            return "EXISTS " + reverse_parser(l[1]) + " " + reverse_parser(l[2])
        else:
            return reverse_parser(l[1]) + " " + l[0] + " " + reverse_parser(l[2])
    else:
        return ""

def p_concept_neg(p):
    'expression : rc IN NOT rc'
    p[0] = ["IN", ["INTER", p[1], p[4]], "BOTTOM"]

def p_expression_in(p):
    'expression : rc IN rc'
    p[0] = ["IN", p[1], p[3]]

def p_expression_equiv(p):
    'expression : rc EQUIV rc'
    p[0] = ["EQUIV", p[1], p[3]]

def p_expression_rin(p):
    'expression : rc RIN rc'
    p[0] = ["RIN", p[1], p[3]]

def p_role_rcomp(p):
    'rc : rc RCOMP rc'
    p[0] = ["RCOMP", p[1], p[3]]

def p_concept_inter(p):
    'rc : rc INTER rc'
    p[0] = ["INTER", p[1], p[3]]

def p_concept_exists(p):
    'rc : EXISTS ID rc'
    p[0] = ["EXISTS", p[2], p[3]]

def p_rc_id(p):
    'rc : ID'
    p[0] = p[1]

def p_rc_bottom(p):
    'rc : BOTTOM'
    p[0] = p[1]

def p_rc_top(p):
    'rc : TOP'
    p[0] = p[1]
#
# def p_rc_paren(p):
#     'rc : LPAREN rc RPAREN'
#     p[0] = p[2]


# def p_concept_exists2(p):
#     'rc : EXISTS LPAREN ID VIRG rc RPAREN'
#     p[0] = ["EXISTS", p[3], p[5]]


def p_error(p):
    # print(p.parser)          # Show parser object
    print(p.lexer)
    if p is not None:
        print("Syntax error in input : %s on line %i, character %i" % (p.__str__(), p.lineno, p.lexpos))
    else:
        print("Syntax error")

# Build the parser
EL_PARSER = yacc.yacc()

if __name__ == "__main__":
    # TODO add proper tests
    tests = [
        "MentalProcess INTER EXISTS hasIntrinsicAbnormalityStatus nonNormal IN ZC2925",
        "CardiacPathology INTER EXISTS hasCause Hypertension IN HypertensiveCardiacPathology"
    ]
    for t in tests:
        print(EL_PARSER.parse(t, lexer=EL_LEXER))
    # result = EL_PARSER.parse('\n')
    # print(result)
