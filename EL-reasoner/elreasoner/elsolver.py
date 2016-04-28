import elnormalizer as norm
import collections as col
import random
import operator

_DEBUG = False


EXST_CAR = "."
NEW_CAR = ":"


def _to_exst_concept(r, c):
    return r + EXST_CAR + c

def _exst_concept_to_rc(c):
    if EXST_CAR not in c:
        return None
    else:
        t = c.split(EXST_CAR)
        return t[0], t[1]



def tract_onto(fname):
    solver = ELSolver()
    # print(list(norm.read_from_file(fname)))
    # print(list(norm.normalize(norm.read_from_file(fname))))
    solver.solve(norm.normalize(norm.read_from_file(fname)))
    solver.dump(fname)

class ELSolver:
    """
    Input the gcis / ris from the normalizer one at a time, with the expected grammar.
    """

    def __init__(self):
        if _DEBUG:
            print("Initiating EL solver")

        self._to_input = list()
        self._concepts = set()

        self._roles = col.defaultdict(set)

        self._roles_already_used = set()

        self._double_entries = col.defaultdict(set)
        # each concept is observed by roles
        self._subsumption_table = col.defaultdict(list)

        # entries who imply this entry
        self._in_edges = col.defaultdict(set)
        # entries implied by this entry
        self._out_edges = col.defaultdict(set)

        # to each entry corresponds its product
        # to each entry : the entries that are contained in its product
        self._roles_inclusions = list()
        self._roles_compositions = list()
        # all relations that have been read so far
        self._gciris = list()
        self._gcirisnum = 0

    def dump(self, fbase):
        with open(fbase + ".normalized", 'w') as f1:
            i = 0
            for g in self._gciris:
                f1.write(str(i) + " : " + str(g) + "\n")
                i += 1
        with open(fbase + ".piles", 'w') as f2:
            for k,v in self._subsumption_table.items():
                f2.write(str(k) + " : " + str(v) + "\n")
        with open(fbase + ".subsumers", 'w') as f3:
            # for k,v in sorted(self._out_edges.items()):
            for k,v in self._subsumption_table.items():
                # f3.write(str(k) + " : " + str(v) + "\n")
                f3.write(str(k) + " : " + str(sorted(set([self._gciris[i][1] for i in v]))) + "\n")

    def solve(self, input):
        for l in input:
            self.input(l)
            while self._to_input != []:
                self.input(self._to_input.pop())

        if _DEBUG:
            print("All input has been read, now handling roles inclusions / compositions")
        # now handle roles inclusions
        for (r,s) in self._roles_inclusions:
            for c in self._roles:
                if r in self._roles[c] and s in self._roles[c]:
                    self._to_input.append(["IN", _to_exst_concept(r, c), _to_exst_concept(s, c)])

        while self._to_input != []:
            self.input(self._to_input.pop())

        for (r,s,t) in self._roles_compositions:
            for c in self._roles:
                if s in self._roles[c] and t in self._roles[c]:
                    conc = self._in_edges[_to_exst_concept(s, c)]
                    for c2 in conc:
                        if c2 in self._roles and r in self._roles[c2]:
                            conc2 = self._in_edges[_to_exst_concept(r, c2)]
                            for c3 in conc2:
                                self._to_input.append(["IN", c3, _to_exst_concept(r, c)])

        while self._to_input != []:
            self.input(self._to_input.pop())

    def _add_concept(self, c):
        """
        Adds a concept and updates carefully the roles that observe this concept.
        """
        if _DEBUG:
            print("Adding concept %s" % c)
        if c not in self._in_edges:
            tp = _exst_concept_to_rc(c)
            if tp is not None:
                self._roles[tp[1]].add(tp[0])


    def _merge_products(self, entry1, entry2):
        """
        Merges e2 in e1.

        Update the edges in the underlying graph structure.
        """
        e1 = self._subsumption_table[entry1]
        e2 = self._subsumption_table[entry2]
        if _DEBUG:
            print("Merging the piles for " + str(entry2) + " into " + str(entry1))
        if e1 == [] or e2 == []:
            print("Warning : empty list !")
            return

        indexe1 = 0
        cond = self._gciris[e2[0]][0]
        if type(cond) == tuple:
            found0 = False
            found1 = False
            while (not found0 or not found1) and indexe1 < len(e1):
                tmp = self._gciris[e1[indexe1]][1]
                if tmp == cond[0]:
                    found0 = True
                if tmp == cond[1]:
                    found1 = True
                indexe1 += 1
        else:
            found = False
            while (not found) and indexe1 < len(e1):
                tmp = self._gciris[e1[indexe1]][1]
                if tmp == cond:
                    found = True
                indexe1 += 1
        # so we known where to insert that product
        for i in e2:
            if i not in e1:
                e1.insert(indexe1, i)
                indexe1 += 1


    def _add_edge(self, e1, e2):
        """
        Add an edge from e1 to e2.
        """
        if not self._has_edge(e1, e2):
            self._out_edges[e1].add(e2)
            self._in_edges[e2].add(e1)
        if e1 != e2:
            if e1 in self._roles and e2 in self._roles:
                for r in self._roles[e1]:
                    if r in self._roles[e2] and (e1, e2) not in self._roles_already_used:
                        self._to_input.append(["IN", _to_exst_concept(r, e1), _to_exst_concept(r, e2)])
                        self._roles_already_used.add((e1, e2))

    def _has_edge(self, e1, e2):
        return e2 in self._out_edges[e1]

    def _add_last_entry(self):
        if self._gcirisnum % 100 == 0:
            print("Added %i entries so far" % self._gcirisnum)
        e = self._gciris[self._gcirisnum-1]
        if _DEBUG:
            print("Adding the entry " + str(e))
        if e[0] not in self._subsumption_table:
            if _DEBUG:
                print(str(e[0]) + " has no subsumers yet")
            if type(e[0]) == tuple:
                self._add_edge(e[0], e[0][0])
                self._add_edge(e[0], e[0][1])

            tmp = self._out_edges[e[0]].copy()
            for i in tmp:
                if i in self._double_entries:
                    for j in self._double_entries[i]:
                        if j in tmp:
                            self._add_edge(e[0], (i,j))
            if type(e[0]) == tuple:
                for f in self._in_edges[e[0][0]] & self._in_edges[e[0][1]]:
                    self._add_edge(f, e[0])

        self._add_edge(e[0], e[0])
        self._add_edge(e[1], e[1])
        self._add_edge(e[0], e[1])

        self._subsumption_table[e[0]].append(self._gcirisnum-1)
            # self._update_entry(e)
        if _DEBUG:
            print("Out edges of " + str(e[1]) + " are currently " + str(self._out_edges[e[1]]))

        if self._subsumption_table[e[1]] != []:
            self._merge_products(e[0], e[1])


        for f1 in self._in_edges[e[0]]:
            self._merge_products(f1, e[0])
            for f2 in self._out_edges[e[1]]:
                self._add_edge(f1, f2)
            self._update_node(f1)



    def _update_node(self, ne):
        """
        An entry has been modified.
        """
        if _DEBUG:
            print("Updating the pile of " + str(ne))
        # self._merge_products(ne, e)

        newlinks = list()

        for x in self._double_entries:
            if x in self._out_edges[ne]:
                for y in self._double_entries[x]:
                    if y in self._out_edges[ne]:
                        if (x,y) not in self._out_edges[ne]:
                            self._add_edge(ne, (x,y))
                            newlinks.append((x,y))
        for (x,y) in newlinks:
            self._merge_products(ne, (x,y))
            self._update_node(ne)

    def input(self, line):
        if _DEBUG:
            print("Input line " + str(line))
        if line[0] == "RIN":
            if type(line[1]) == list and "RCOMP" in line[1]:
                self._roles_compositions.append( (line[1][1], line[1][2], line[2]) )
            else:
                self._roles_inclusions.append( (line[1], line[2])  )

        if line[0] == "IN":
            if type(line[1]) == list and line[1][0] == "INTER":
                c11 = line[1][1]
                c12 = line[1][2]
                self._add_concept(c11)
                self._add_concept(c12)
                c1 = tuple(sorted((line[1][1], line[1][2])))

                self._double_entries[c1[0]].add(c1[1])
            else:
                c1 = line[1]
                self._add_concept(c1)
            c2 = line[2]
            self._add_concept(c2)
            self._gcirisnum += 1
            self._gciris.append((c1, c2))
            self._add_last_entry()

if __name__ == "__main__":


    def produce_test_instance(nb):
        for i in range(nb):
            yield(["IN", "C" + str(i), "C" + str(i+1)])

    # tract_onto("t2.el")
    def test1():
        import time
        t1 = time.clock()

        tmp = list(produce_test_instance(100))
        solver = ELSolver()
        random.shuffle(tmp)
        solver.solve(tmp)
        solver.dump("test")
        print(time.clock() - t1)

    import time
    t1 = time.clock()
    # test1()
    tract_onto("go/go.tex.el")
    # tract_onto("t2.el")
    print(time.clock() - t1)
