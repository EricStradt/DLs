"""
@file hh_solver.py
@author André Schrottenloher

@brief The most simple Horn-Horn set constraints solver.

"""

import copy
import hh_util

_DEBUG = False

def get_units(clauses):
    return set([c for c in clauses if clauses[c][1] == []])

def _inner_resolve(clauses, units):
    """
    Modifies clauses and units in place.

    >>> _inner_resolve({1: ('x3', ['x1']), 2: ('x3', []), 4: ('x0', ['x0', 'x2']),
    5: ('x3', ['x4']), 6: ('x3', ['x4']), 7: ('x3', ['x0', 'x2']), 8: ('x1', []),
    9: ('x0', ['x0']), 10: ('x0', ['x1', 'x0']), 11: ('x1', ['x1']), 12: ('x4', ['x3']),
    13: ('x0', ['x3']), 14: ('x2', ['x0'])}, {8, 2})

    """
    if _DEBUG or hh_util.VERBOSE:
        print("-------------------------------")
        print("Solving the set of clauses : " + str(clauses))
        print("Units are : " + str(units))
    keepon = True
    newunits = set(units)
    while keepon:
        keepon = False
        to_remove = set()
        tmp = set()
        # look on all clauses
        for c in clauses:
            if c not in units:
                for u in newunits:
                    # if the unit u occurs in this clause, remove the clause
                    if clauses[u][0] == clauses[c][0]:
                        to_remove.add(c)
                    # if the literal's negation occurs, then remove it from the clause
                    elif clauses[u][0] in clauses[c][1]:
                        clauses[c][1].remove(clauses[u][0])
                    # if it happens that the clause has no more negative literal...
                    if clauses[c][1] == []:
                        # it is empty ? failure
                        if clauses[c][0] == None:
                            return False
                        # if not, it is a new unit. We will go back on it on the next loop.
                        units.add(c)
                        tmp.add(c)
                        keepon = True
        # remove all the clauses that we said we had to remove
        for c in to_remove:
            # if _DEBUG:
                # print("Removing clause " + str(c))
            clauses.pop(c)
            if c in units:
                units.remove(c)
        # prepare the units that we are going to check for
        newunits = tmp.difference(to_remove)

    # loop has ended : this is satisfiable. Moreover, all the literals corresponding
    # to the unit clauses are evaluated to True.
    if _DEBUG or hh_util.VERBOSE:
        print("This is true. ")
        print("Final set of clauses : " + str(clauses))
        print("Units are : " + str(units))
    return True



def _implies(clauses, units, newc):
    """
    Answers the question "does the current set of clauses and units imply
    this clause ?".

    This method is very similar to _inner_resolve, but it leaves its arguments
    unchanged, by keeping separately the changes to the set of clauses. In
    the best case, those changes will be minimal, in the worst case, this method
    could use as much as memory that is already used to store the clauses.

    @param clauses The set of clauses
    @param units The current units in these clauses. It is supposed to be up-to-date.
    @param newc The clause which we have to determine if it is "implied" or not.

    @return True if the clause is implied, else false.
    """

    if _DEBUG or hh_util.VERBOSE:
        print("-------------------------------")
        print("Checking if the set of clauses " + str(clauses))
        print("implies " + str(newc))

    if _DEBUG:
        hh_util.check_ic(newc)
    keepon = True

    # internal changes in units
    iunits = units.copy()
    # internal changes in clauses
    iclauses = dict()
    # internal removings of clauses
    removed = set()
    # iunits.add(-1)

    allkeys = set(clauses.keys())
    iclauses[-1] = (None, [newc[0]])
    allkeys.add(-1)
    # new positive units

    newunits = set()
    newunits |= units

    for i in range(len(newc[1])):
        iclauses[-2 - i] = (newc[1][i], [])
        allkeys.add(-2-i)
        newunits.add(-2-i)
        iunits.add(-2 - i)

    while keepon:
        keepon = False
        # tmp : temporary variable for new units
        tmp = set()
        # look on all clauses
        # print(iclauses)
        for c in allkeys:
            if c not in iunits and c not in removed:
                # if c corresponds to an already modified clause
                cl = iclauses[c] if c in iclauses else clauses[c]
                # print("Studying clause " + str(cl))
                for u in newunits:
                    # if the unit u occurs in this clause, remove the clause
                    theunit = iclauses[u] if u in iclauses else clauses[u]
                    if theunit[0] == cl[0]:
                        removed.add(c)
                        # to_remove.add(c)
                    # if the literal's negation occurs, then remove it from the clause
                    elif theunit[0] in cl[1]:
                        if c not in iclauses:
                            iclauses[c] = copy.deepcopy(clauses[c])#.copy()
                            cl = iclauses[c]
                        cl[1].remove(theunit[0])
                    if cl[1] == []:
                        if cl[0] == None:
                            if _DEBUG or hh_util.VERBOSE: print("The answer is yes.")
                            return True
                        # if not, it is a new unit. We will go back on it on the next loop.
                        iunits.add(c)
                        tmp.add(c)
                        keepon = True

        # prepare the units that we are going to check for
        newunits = tmp.difference(removed)
    # loop has ended : this is satisfiable. Moreover, all the literals corresponding
    # to the unit clauses are evaluated to True.
    if _DEBUG or hh_util.VERBOSE: print("The answer is no.")
    return False



def list_to_dict(elts):
    i = 0
    res = dict()
    for e in elts:
        res[i] = e
        i += 1
    return res


class SimpleSolver:
    """
    @class SimpleSolver
    @brief The most simple Horn-Horn set constraints solver.

    The worst-case complexity of this solver is cubic in the size of the formula.
    However, it could be upgraded to quadratic by making a good choice
    of questions.

    """

    def __init__(self):
        self._outer_units = dict()
        self._inner_units = set()
        self._outer_clauses = list()

    def input(self, oclauses):
        """
        Inputs a set of clauses, parsed by the HH_PARSER.
        Warning : some of them could be None (syntax error or comments). They have
        to be dismissed here.

        @param oclauses An iterable of (parsed) outer clauses
        """
        self._outer_clauses = list_to_dict( [o for o in oclauses if o is not None] )
        if _DEBUG:
            for c in self._outer_clauses:
                hh_util.check_oc(self._outer_clauses[c])

    def solve(self):
        """
        solves the current Horn-Horn instance.

        @return True of False.
        """
        if _DEBUG or hh_util.VERBOSE:
            print("======================")
            print("Solving : ")
            print(self._outer_clauses)
        self._outer_units = dict()

        for u in get_units(self._outer_clauses):
            self._outer_units[u] = self._outer_clauses[u][0]

        if _DEBUG or hh_util.VERBOSE:
            print("Outer units are " + str(self._outer_units))

        self._inner_units = get_units(self._outer_units)

        # The variable repeat is True as long as a new (outer) unit has been found.
        repeat = True
        while repeat:
            newunits = set()
            repeat = False
            if not _inner_resolve(self._outer_units, self._inner_units):
                if _DEBUG or hh_util.VERBOSE:
                    print("========================")
                    print("Done solving. This is False.")
                return False

            # try to eliminate negative terms in outer clauses
            for c in self._outer_clauses:
                if c not in self._outer_units:
                    negterms = self._outer_clauses[c][1]
                    remove = []
                    for t in negterms:
                        if _implies(self._outer_units, self._inner_units, t):
                            remove.append(t)
                    for t in remove:
                        if _DEBUG or hh_util.VERBOSE:
                            print("Removing term " + str(t))
                        negterms.remove(t)
                    if negterms == []:
                        # if this term is implied by the current set of outer units,
                        # this is fine. We can remove it from its outer clause.
                        # self._outer_clauses[c][1].pop()
                        # but, wait, we could have obtained a unit, then.
                        # if self._outer_clauses[c][1] == []:
                            # if the clause is not a unit, but is empty, we just have proven
                            # false.
                        if self._outer_clauses[c][0] is None:
                            if _DEBUG or hh_util.VERBOSE:
                                print("========================")
                                print("Done solving. This is False.")
                            return False
                        else:
                            # otherwise, we have a new outer unit.
                            if _DEBUG or hh_util.VERBOSE:
                                print("There is a new (outer) unit : " + str(self._outer_clauses[c][0]))
                            self._outer_units[c] = self._outer_clauses[c][0]
                            # newunits.add(c)
                    # units.add(c)
                            repeat = True
            # self._outer_units |= newunits

        if _DEBUG or hh_util.VERBOSE:
            print("========================")
            print("Done solving. This is True.")
        return True

if __name__ == "__main__":
    pass
