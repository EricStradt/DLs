"""
@package EL-reasoner

Tools for reasoning on EL/EL+ ontologies.

"""

import parsers
import elreasoner.elnormalizer as norm
import elreasoner.elsolver as classifier

if __name__ == "__main__":

    import sys
    import time
    import math

    if sys.argv[1] == "normalize":
        if len(sys.argv) >= 3:
            if sys.argv[2].endswith(".owl"):
                input_syntax = "owl"
            elif sys.argv[2].endswith(".el"):
                input_syntax = "el"
            else:
                input_syntax = "el" if len(sys.argv) == 3 else sys.argv[3]

            output_syntax = "el" if len(sys.argv) <= 4 else sys.argv[4]

            print("Input syntax is %s" % input_syntax)
            print("Output syntax if %s" % output_syntax)
            print("Normalizing file %s" % sys.argv[2])

            t1 = time.clock()

            if input_syntax == "owl":
                onto = parsers.owl_parse(sys.argv[2])
            elif input_syntax == "el":
                onto = parsers.el_parse(sys.argv[2])

            if output_syntax == "owl":
                parsers.owl_write(sys.argv[2] + ".normalized", norm.normalize(onto))
            elif output_syntax == "el":
                parsers.el_write(sys.argv[2] + ".normalized", norm.normalize(onto))

            print("The operation took %f seconds." % (time.clock() - t1))
            sys.exit()

    elif sys.argv[1] == "classify":
        # import parsers.el.elparser as test
        #
        # print(test.EL_PARSER.parse("MentalProcess INTER EXISTS hasIntrinsicAbnormalityStatus nonNormal IN ZC2925"))
        # sys.exit()
        if len(sys.argv) >= 3:
            fname = sys.argv[2]
            output = sys.argv[3] if len(sys.argv) >= 4 else "classification"
            if not fname.endswith(".normalized"):
                print("Warning : the file to classify is named %s" % fname)
                print("Are you sure that this is a normalized ontology ?")

            solver = classifier.ELSolver()
            t1 = time.clock()
            solver.solve(parsers.el_parse(sys.argv[2]))
            solver.dump(output)

            print("Output written to %s" % output)
            print("The operation took %f seconds." % (time.clock() - t1))
            sys.exit()

    elif sys.argv[1] == "describe":

        if len(sys.argv) >= 3:
            fname = sys.argv[2]
            if fname.endswith(".normalized"):
                print("This is a normalized ontology")

            if fname.endswith(".subsumers"):
                print("This file contains all subsumption relationships between concepts \
                    and pairs of concepts in an ontology")
            if fname.endswith(".piles"):
                print("This file contains piles. Each one corresponds to a concept.\
                    Its subsumers are sorted in subsumption order, and the\
                    numbers refer to the GCIs that allowed subsumption.")
            sys.exit()
