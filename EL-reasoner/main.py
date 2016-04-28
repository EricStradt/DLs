"""
@package EL-reasoner

Tools for reasoning on EL/EL+ ontologies.

"""

import parsers
import elreasoner.elnormalizer as norm

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

            print("The operation took %f milliseconds." % (time.clock() - t1))
