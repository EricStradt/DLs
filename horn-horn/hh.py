"""
@file hh.py
@brief putting together the files in the module (apart from tests)

"""

try:
    import hh_lexer
    import hh_parser
except Exception as e:
    pass

import json
import hh_solver
import hh_util
import hh_test


def _help():
    h_str = """
    Usage :
    - generate xxx n k p
    Generates a small example file named xxx, with n clauses of max size
    k, on p literals.
    Default values : xxx = example.clauses, n = 7, k = 9, p = 7
    - generateraw xxx n k p
    Does basically the same thing, but serializes python objects to JSON
    (no special syntax)
    - solve xxx (verbose)
    Parses the file xxx and solves it. "verbose" or "v" specifies the verbose
    state.
    - solveraw xxx (verbose)
    Same thing as solve, but reads python JSON objects (no special syntax).
    - help
    Displays this help.
    All tests are in the file hh_test.py and can be runned from the command
    line.

    Example usage :
    python3 hh.py generate test.clauses 10
    python3 hh.py solve test.clauses verbose
    """
    print("========================")
    print(h_str)


if __name__ == "__main__":

    import sys
    import time
    import math

    if len(sys.argv) < 2:
        _help()
        sys.exit()

    if sys.argv[1] == "generate":
        if len(sys.argv) >= 3:
            fname = sys.argv[2]
        else:
            fname = "example.clauses"
        if len(sys.argv) >= 4:
            nb = int(sys.argv[3])
        else:
            nb = 7
        if len(sys.argv) >= 5:
            size = int(sys.argv[4])
        else:
            size = 9
        if len(sys.argv) >= 6:
            lits = int(sys.argv[5])
        else:
            lits = 7
        with open(fname, 'w') as f:
            f.write("# This file was generated with hh.py.\n")
            f.write("# It contains Horn-Horn set constraints.\n")
            f.write("# The syntax should be simple. See the documentation if needed.\n")
            for oc in hh_test.generate_outer_formula(int(math.sqrt(size)), int(math.sqrt(size)), lits, nb):
                f.write(hh_util.reverse_parser_outer(oc) + "\n")
        sys.exit()
    elif sys.argv[1] == "generateraw":
        if len(sys.argv) >= 3:
            fname = sys.argv[2]
        else:
            fname = "example.clauses"
        if len(sys.argv) >= 4:
            nb = int(sys.argv[3])
        else:
            nb = 7
        if len(sys.argv) >= 5:
            size = int(sys.argv[4])
        else:
            size = 9
        if len(sys.argv) >= 6:
            lits = int(sys.argv[5])
        else:
            lits = 7
        with open(fname, 'w') as f:
            f.write("# This file was generated with hh.py.\n")
            f.write("# It contains Horn-Horn set constraints.\n")
            f.write("# They are here in their internal representation (tuples), parsed to JSON.\n")
            for oc in hh_test.generate_outer_formula(int(math.sqrt(size)), int(math.sqrt(size)), lits, nb):
                f.write(json.dumps(oc) + "\n")
        sys.exit()
    elif sys.argv[1] == "solve":
        if len(sys.argv) >= 3:
            fname = sys.argv[2]
            solver = hh_solver.SimpleSolver()
            if len(sys.argv) == 4 and "v" in sys.argv[3]:
                hh_util.VERBOSE = True
            with open(fname, 'r') as f:
                solver.input([hh_parser.HH_PARSER.parse(c) for c in f])
            t1 = time.clock()
            b = solver.solve()
            print("The result is %i. The computation took %f milliseconds." % (b, 1000 * (time.clock() - t1)))
            sys.exit()
    elif sys.argv[1] == "solveraw":
        if len(sys.argv) >= 3:
            fname = sys.argv[2]
            solver = hh_solver.SimpleSolver()
            if len(sys.argv) == 4 and "v" in sys.argv[3]:
                hh_util.VERBOSE = True
            with open(fname, 'r') as f:
                solver.input([json.loads(c) for c in f if "#" not in c])
            t1 = time.clock()
            b = solver.solve()
            print("The result is %i. The computation took %f milliseconds." % (b, 1000 * (time.clock() - t1)))
            sys.exit()
    _help()
