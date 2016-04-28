# ------------------------------------------------------------
# elnormalizer.py
#
# Normalizer for El / EL+
# ------------------------------------------------------------

from elparser import EL_PARSER

INC_CAR = ","
EXST_CAR = "."
NEW_CAR = ":"


def _is_simple(c):
    if type(c) == str:
        return True
    elif c[0] == "EXISTS" and type(c[2]) == str:
        return True
    return False


def _to_exst_concept(r, c):
    return r + EXST_CAR + c

def _exst_concept_to_rc(c):
    if EXST_CAR not in c:
        return None
    else:
        t = c.split(EXST_CAR)
        return t[0], t[1]

def simplify(l, new_concept_name, new_role_name):
    """
    Simplifies a line that is already parsed by the parser.

    At the end of the process, all GCIs are of the form :
    ["IN", C1, C2]
    ["IN", ["INTER", C1, C2], C3]
    ["IN", C3, ["INTER", C1, C2]]

    Where the Ci are names.
    Simple existential quantified concepts are already replaced by new names.

    All RIs are :
    ["RIN", ["RCOMP", r1, r2], r3]
    ["RIN", r3, ["RCOMP", r1, r2]]
    ["RIN", r1, r2]

    """
    if l[0] == "EQUIV":
        return False, [ ["IN", l[1], l[2]], ["IN", l[2], l[1]] ]
    if l[0] == "IN":
        c1 = l[1]
        c2 = l[2]
        if not _is_simple(c1):
            if c1[0] == "INTER":
                c11 = c1[1]
                c12 = c1[2]
                if not _is_simple(c11):
                    return False, [  ["IN", c11, new_concept_name], ["IN", ["INTER", c12, new_concept_name], c2] ]
                elif not _is_simple(c12):
                    return False, [  ["IN", c12, new_concept_name], ["IN", ["INTER", c11, new_concept_name], c2] ]
                if _is_simple(c2):
                    nc11 = _to_exst_concept(c11[1], c11[2]) if type(c11) != str and c11[0] == "EXISTS" else c11
                    nc12 = _to_exst_concept(c12[1], c12[2]) if type(c12) != str and c12[0] == "EXISTS" else c12
                    return True, [ ["IN", ["INTER", nc11, nc12], c2] ]
            # complex existential quantification
            elif c1[0] == "EXISTS":
                r = c1[1]
                c11 = c1[2]
                return False, [  ["IN", c11, new_concept_name], ["IN", ["EXISTS", r, new_concept_name], c2] ]
        if not _is_simple(c2):
            if c2[0] == "INTER":
                c21 = c2[1]
                c22 = c2[2]
                return False, [ ["IN", c1, c21], ["IN", c1, c22] ]
            elif c2[0] == "EXISTS":
                r = c2[1]
                c21 = c2[2]
                return False, [  ["IN", c1, ["EXISTS", r, new_concept_name]], ["IN", new_concept_name, c21] ]
        nc1 = _to_exst_concept(c1[1], c1[2]) if type(c1) != str and c1[0] == "EXISTS" else c1
        nc2 = _to_exst_concept(c2[1], c2[2]) if type(c2) != str and c2[0] == "EXISTS" else c2
        return True, [ ["IN", nc1, nc2] ]
    if l[0] == "RIN":
        r1 = l[1]
        r2 = l[2]
        if type(r1) != str and r1[0] == "RCOMP":
            r11 = r1[1]
            r12 = r1[2]
            if type(r11) != str:
                return False, [ ["RIN", r11, new_role_name], ["RIN", ["RCOMP", new_role_name, r12], r2] ]
            elif type(r12) != str:
                return False, [ ["RIN", r12, new_role_name], ["RIN", ["RCOMP", r11, new_role_name], r2] ]
    # default : this is already normalized
    return True, [ l ]


def simplify_closure(line, count):
    simpl = []
    lines = [line]
    while lines != []:
        tmp = []
        for line in lines:
            b, new = simplify(line, NEW_CAR + "C" + str(count), NEW_CAR + "R" + str(count))
            if b:
                simpl += new
            else:
                count += 1
                tmp += new
        lines = tmp
    return count, simpl

def normalize(lines):
    """
    Normalizes but still does not write horn clauses. Returns all GCIs / RIs (separates both)
    """
    count = 1
    for line in lines:
        count, l = simplify_closure(line, count)
        for newline in l:
            yield newline


# ---------------------------------------------------
# Reading / writing files
# ---------------------------------------------------

def _line_to_str(l):
    if type(l) == str:
        return l
    elif type(l) == list:
        return _line_to_str(l[1]) + " " + l[0] + " " + _line_to_str(l[2])
    else:
        return ""

def read_from_file(filename):
    with open(filename, 'r') as f:
        for l in f:
            if len(l) > 2 and "#" not in l:
                tmp = EL_PARSER.parse(l)
                if tmp is not None:
                    yield tmp

def write_to_file(filename, ls):
    with open(filename, 'w') as f:
        for l in ls:
            f.write(_line_to_str(l) + "\n")

def normalize_file(filename):
    write_to_file(filename + ".normal", normalize(read_from_file(filename)))

if __name__ == "__main__":
    normalize_file("galen/galen.tex.el")
    # o = list(read_from_file("test2.el"))
    # print(o)
    # res = normalize(o)
    # print(res)
    # write_to_file("test2.el.normalized", res[0] + res[1])
