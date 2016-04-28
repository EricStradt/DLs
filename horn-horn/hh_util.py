"""
@file hh_util.py
@author André Schrottenloher

@brief Utilities for the hh module.

"""
from hh_parser import HH_PARSER


_DEBUG = True

##############################
# Determines the VERBOSE state of solvers.
#################################

VERBOSE = False


def check_ic(inner_clause):
    """
    Check if that thing is an inner clause (with the expected form)
    For debugging purposes only.

    >>> check_ic((None, ['C1', 'C2']))
    """
    try:
        assert type(inner_clause) == tuple
        assert len(inner_clause) == 2
        assert inner_clause[0] is None or type(inner_clause[0]) == str
        assert type(inner_clause[1]) == list
        assert inner_clause[0] is not None or inner_clause[1] != []
    except Exception as e:
        raise ValueError(inner_clause)


def check_oc(outer_clause):
    """

    >>> check_oc(((None, ['C1', 'C2']), []))
    """
    try:
        assert type(outer_clause) == tuple
        assert len(outer_clause) == 2
        assert outer_clause[0] is None or type(outer_clause[0]) == tuple
        assert type(outer_clause[1]) == list
        assert outer_clause[0] is not None or outer_clause[1] != []
    except Exception as e:
        raise ValueError(outer_clause)

def reverse_parser_inner(inner_clause):
    if _DEBUG:
        check_ic(inner_clause)
    if inner_clause[1] == []:
        return "TOP IN " + inner_clause[0]
    ltmp = ""
    for i in range(len(inner_clause[1]) - 1):
        ltmp += inner_clause[1][i] + " INTER "
    ltmp += inner_clause[1][len(inner_clause[1]) - 1]
    if inner_clause[0] is None:
        ltmp += " IN BOTTOM"
    else:
        ltmp += " IN " + inner_clause[0]
    return ltmp

def reverse_parser_outer(outer_clause):
    """
    >>> reverse_parser_outer(HH_PARSER.parse("TRUE IMPLIES C1 INTER C2 IN BOTTOM"))
    'TRUE IMPLIES C1 INTER C2 IN BOTTOM'
    """
    if _DEBUG:
        check_oc(outer_clause)
    if outer_clause[1] == []:
        return "TRUE IMPLIES " + reverse_parser_inner(outer_clause[0])
    ltmp = ""
    for i in range(len(outer_clause[1]) - 1):
        ltmp += reverse_parser_inner(outer_clause[1][i]) + " AND "
    ltmp += reverse_parser_inner( outer_clause[1][len(outer_clause[1]) - 1] )
    if outer_clause[0] is None:
        ltmp += " IMPLIES FALSE"
    else:
        ltmp += " IMPLIES " + reverse_parser_inner(outer_clause[0])
    return ltmp


class DefaultSolver:

    def __init__(self):
        pass

    def input(self, outer_clauses):
        pass

    def solve(self):
        return False


if __name__ == "__main__":
    import doctest
    # check_ic((None, ['C1', 'C2']))
    doctest.testmod()
