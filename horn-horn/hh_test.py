"""
@file horn-test.py
@author André Schrottenloher

Testing a Horn-Horn solver.
"""

import random
import hh_util
import glob
import time
import hh_solver
import hh_parser
import os


#########################################
# Generating random Horn-Horn formulas
#########################################


def generate_inner_clause(maxsizei, literals, isneg=0.2):
    size = random.randrange(maxsizei)
    if random.random() < isneg:
        return (None, [literals[random.randrange(len(literals))] for i in range(size + 1)] )
    else:
        return (literals[random.randrange(len(literals))],
            [literals[random.randrange(len(literals))] for i in range(size + 1)] )



def generate_outer_formula(maxsizeo, maxsizei, nblits, nbo, isneg=0.2):
    lits = ["x" + str(i) for i in range(nblits)]
    for i in range(nbo):
        size = random.randrange(maxsizeo)
        if random.random() < isneg:
            yield (None,
                    [generate_inner_clause(maxsizei, lits) for j in range(size + 1)] )
        else:
            yield (generate_inner_clause(maxsizei, lits),
                    [generate_inner_clause(maxsizei, lits) for j in range(size)] )

#######################################################


def generate_tests(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for maxsizeo in [2,3,4,5]:
        for maxsizei in [4,5,6]:
            for nblits in [5,6,7]:
                for nbo in [5,10]:
                    with open(("%s/%i-%i-%i-%i.clauses") % (dirname, maxsizeo, maxsizei, nblits, nbo), 'w') as f:
                        f.write("%i %i %i %i\n" % (maxsizeo, maxsizei, nblits, nbo))
                        for oc in generate_outer_formula(maxsizeo, maxsizei, nblits, nbo):
                            f.write(hh_util.reverse_parser_outer(oc) + "\n")
    print("Tests instances written to %s" % dirname)


def _read_test_file(fname):
    first = ""
    isfirst = True
    other = []
    with open(fname, 'r') as f:
        for l in f:
            if isfirst:
                first = l
                isfirst = False
            else:
                other.append(l)
    return first, other

def test_solver(dirname, solver, doestime=False):
    """
    Test for comparison between two solvers.
    """
    results = "%s/results-%s.txt" % (dirname, solver.__name__)
    with open(results, 'w') as res:
        res.write("Maxsizeo maxsizei nblits nbouterclauses result time\n")
        for f in sorted(glob.glob("%s/*.clauses" % dirname)):
            print("Testing file %s" % f)
            t1 = time.clock()
            l, clauses = _read_test_file(f)
            s = solver()
            s.input([hh_parser.HH_PARSER.parse(c) for c in clauses])
            b = s.solve()
            if doestime:
                res.write(l[:len(l) - 1] + "  " + str(b) + "  " +  str(time.clock() - t1) + "\n")
            else:
                res.write(l[:len(l) - 1] + "  " + str(b) + "\n")
    print("Done testing")

##################################################

def search_proportion_true(maxsizeo, maxsizei, nblits, nbo, isnego, nbtests=200):
    """
    Returns the mean time taken and the proportion true.
    """
    restrue = 0
    totaltime = 0
    for i in range(nbtests):
        t1 = time.clock()
        s = hh_solver.SimpleSolver()
        s.input(generate_outer_formula(maxsizeo, maxsizei, nblits, nbo, isnego))
        if s.solve():
            restrue += 1
        totaltime += time.clock() - t1
    return totaltime / nbtests, restrue / nbtests
    # print("Mean time : " + str(totaltime / nbtests))
    # print("Proportion of true : " + str(restrue / nbtests))

def write_timer_and_prop(fname):
    with open(fname, 'w') as f:
        for maxsizeo in [2, 5, 10, 20]:
            print("Still working...")
            for maxsizei in [2, 5, 10, 20, 30]:
                for nblits in [2, 5, 10, 20, 30]:
                    for nbo in [2, 5, 10, 20, 30]:
                        for isnego in [0.1]:
                            a,b = search_proportion_true(maxsizeo, maxsizei, nblits, nbo, isnego, 50)
                            f.write(str(maxsizeo) + "\t" + str(maxsizei) + "\t" + str(nblits) + "\t" + str(nbo) + "\t" + str(a) + "\t" + str(b) + "\n")

def _help():
    h_str = """
    Usage :
    - generate xxx
    Writes a bunch of tests to the folder xxx
    - test xxx
    Tests in the folder xxx
    - means xxx
    Computes some mean times of solving and writes to the file xxx
    - help
    Displays this help.
    """
    print("========================")
    print(h_str)

if __name__ == "__main__":

    import sys

    if sys.argv[1] == "generate":
        if len(sys.argv) == 3:
            generate_tests(sys.argv[2])
    elif sys.argv[1] == "test":
        if len(sys.argv) == 3:
            test_solver(sys.argv[2], hh_solver.SimpleSolver)
    elif sys.argv[1] == "means":
        if len(sys.argv) == 3:
            write_timer_and_prop(sys.argv[2])
    elif sys.argv[1] == "help":
        _help()
    else:
        _help()
