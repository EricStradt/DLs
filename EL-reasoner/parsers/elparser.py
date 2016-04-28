# ------------------------------------------------------------
# elparser.py
#
# Parser for a small EL / EL+ syntax
# code adapted from http://www.dabeaz.com/ply/ply.html#ply_nn23
# ------------------------------------------------------------

import ply.yacc as yacc

from ellexer import tokens

# ------------------------------------------------------------

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

def p_rc_id(p):
    'rc : ID'
    p[0] = p[1]

def p_rc_bottom(p):
    'rc : BOTTOM'
    p[0] = p[1]

def p_rc_top(p):
    'rc : TOP'
    p[0] = p[1]

def p_rc_paren(p):
    'rc : LPAREN rc RPAREN'
    p[0] = p[2]

def p_concept_exists(p):
    'rc : EXISTS ID rc'
    p[0] = ["EXISTS", p[2], p[3]]

def p_concept_exists2(p):
    'rc : EXISTS LPAREN ID VIRG rc RPAREN'
    p[0] = ["EXISTS", p[3], p[5]]


def p_error(p):
    if p is not None:
        print("Syntax error in input : %s on line %i, character %i" % (p.__str__(), p.lineno, p.lexpos))
    else:
        print("Syntax error")

# Build the parser
EL_PARSER = yacc.yacc()

if __name__ == "__main__":
    result = EL_PARSER.parse('EXISTS(r, EXISTS(s, C1)) INTER C2 INTER EXISTS(s, C3) IN C5\n')
    print(result)
