"""
@file elsolver.py
@author André Schrottenloher
@date April 2016
@brief Classifier for EL/EL+.

Usage :
@code
solver = ELSolver()
solver.solve(inputdata)
solver.dump(fname)
@endcode

"""

try:
    import elnormalizer as norm
except ImportError as e:
    import elreasoner.elnormalizer as norm


import collections as col
import random
import operator
import time

_TIME = True
_DEBUG = False
VERBOSE = True

EXST_CAR = "."

# TODO refactor utils

def _to_exst_concept(r, c):
    return r + EXST_CAR + c

def _exst_concept_to_rc(c):
    if EXST_CAR not in c:
        return None
    else:
        t = c.split(EXST_CAR)
        return t[0], t[1]

def treat(concept):
    if type(concept) == list and concept[0] == "EXISTS":
        return _to_exst_concept(concept[1], concept[2])
    else:
        return concept

##########################

class ELSolver:
    """
    Input the gcis / ris from the normalizer one at a time, with the expected grammar.
    """

    def __init__(self):
        if _DEBUG:
            print("Initiating EL solver")

        self._to_input = list()
        self._concepts = col.defaultdict(set)

        self._roles = col.defaultdict(set)
        self._inter_roles = col.defaultdict(set)

        # self._roles_already_used = set()

        self._double_entries = col.defaultdict(set)
        # each concept is observed by roles
        self._subsumption_table = col.defaultdict(list)

        # entries who imply this entry
        self._in_edges = col.defaultdict(set)
        # entries implied by this entry
        self._out_edges = col.defaultdict(set)

        self._new_out_edges = col.defaultdict(set)

        # to each entry corresponds its product
        # to each entry : the entries that are contained in its product
        self._roles_inclusions = list()
        self._roles_compositions = list()
        # all relations that have been read so far
        self._gciris = list()
        self._gcirisnum = 0
        if _TIME:
            self._merging_time = 0
            self._total_time = 0
            self._time_add_edge = 0
            self._time_lookups = 0
            self._time_roles = 0

    def dump(self, fbase):
        with open(fbase + ".normalized", 'w') as f1:
            i = 0
            for g in self._gciris:
                f1.write(str(i) + " : " + str(g) + "\n")
                i += 1
        l1 = sorted([(k,v) for (k,v) in self._subsumption_table.items() if type(k) == str])
        l2 = sorted([(k,v) for (k,v) in self._subsumption_table.items() if type(k) == tuple])
        with open(fbase + ".piles", 'w') as f2:
            for k,v in l1:
                f2.write(str(k) + " : " + str(v) + "\n")
            for k,v in l2:
                f2.write(str(k) + " : " + str(v) + "\n")
        # l1 = sorted([(k,v) for (k,v) in self._out_edges.items() if type(k) == str])
        # l2 = sorted([(k,v) for (k,v) in self._out_edges.items() if type(k) == tuple])
        with open(fbase + ".subsumers", 'w') as f3:
            for k,v in l1:
                f3.write(str(k) + " : " + str(sorted(set([self._gciris[i][1] for i in v]))) + "\n")
            for k,v in l2:
                f3.write(str(k) + " : " + str(sorted(set([self._gciris[i][1] for i in v]))) + "\n")
            # for k,v in l1:
            #     f3.write(str(k) + " : " + str(v) + "\n")
            # for k,v in l2:
            #     f3.write(str(k) + " : " + str(v) + "\n")

    def solve(self, input, limitto=1000000):
        if _TIME:
            t1 = time.clock()

        counter = 0
        for l in input:
            counter += 1
            self.input(l)
            while self._to_input != []:
                self.input(self._to_input.pop())
            if counter > limitto:
                break

        print("All input has been read, now handling roles inclusions / compositions")

        print("There are %i double entries" % len(self._double_entries))
        t2 = time.clock()
        print("There are %i entries in self._roles" % len(self._roles))
        # now handle roles inclusions

        for r in self._concepts:
            for c in self._concepts[r]:
                for c2 in self._concepts[r] & self._out_edges[c]:
                    self._to_input.append(["IN", _to_exst_concept(r, c), _to_exst_concept(r, c2)])
        # if e1 != e2:
        #     if e1 in self._roles and e2 in self._roles:
        #         for r in self._roles[e1]:
        #             if r in self._roles[e2] and (e1, e2) not in self._roles_already_used:
        #                 self._to_input.append(["IN", _to_exst_concept(r, e1), _to_exst_concept(r, e2)])
        #                 self._roles_already_used.add((e1, e2))

        for (r,s) in self._roles_inclusions:
            for c in self._concepts[r] & self._concepts[s]:
                self._to_input.append(["IN", _to_exst_concept(r, c), _to_exst_concept(s, c)])
            # for c in self._roles:
            #     if r in self._roles[c] and s in self._roles[c]:
            #         self._to_input.append(["IN", _to_exst_concept(r, c), _to_exst_concept(s, c)])

        while self._to_input != []:
            self.input(self._to_input.pop())

        for (r,s,t) in self._roles_compositions:
            for c in self._concepts[s] & self._concepts[t]:
                conc = self._in_edges[_to_exst_concept(s, c)]
                for c2 in conc:
                    if c2 in self._roles and r in self._roles[c2]:
                        conc2 = self._in_edges[_to_exst_concept(r, c2)]
                        for c3 in conc2:
                            self._to_input.append(["IN", c3, _to_exst_concept(r, c)])

        while self._to_input != []:
            self.input(self._to_input.pop())

        self._time_roles = time.clock() - t2

        if _TIME:
            self._total_time += time.clock() - t1
            print("Total time was " + str(self._total_time))
            print("I spent the following for roles (inclusions, etc) : " + str(self._time_roles))
            print("I spent the following for pile merging : " + str(self._merging_time))
            print("I spent the following for adding edges : " + str(self._time_add_edge))
            print("I spent the following for double entries lookup : " + str(self._time_lookups))

    def _add_concept(self, c):
        """
        Adds a concept and updates carefully the roles that observe this concept.
        """
        if _DEBUG:
            print("Adding concept %s" % c)
        if c not in self._in_edges:
            tp = _exst_concept_to_rc(c)
            if tp is not None:
                self._concepts[tp[0]].add(tp[1])
                self._roles[tp[1]].add(tp[0])


    def _merge_products(self, entry1, entry2):
        """
        Merges e2 in e1.

        Update the edges in the underlying graph structure.
        """
        # return
        if _TIME:
            t1 = time.clock()
        e1 = self._subsumption_table[entry1]
        e2 = self._subsumption_table[entry2]
        if _DEBUG:
            print("Merging the piles for " + str(entry2) + " into " + str(entry1))
        if e1 == [] or e2 == []:
            # print("Warning : empty list !")
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
        if _TIME:
            self._merging_time += time.clock() - t1

    def _add_edge(self, e1, e2):
        """
        Add an edge from e1 to e2.
        """
        if _TIME:
            t1 = time.clock()
        if not self._has_edge(e1, e2):
            self._out_edges[e1].add(e2)
            self._in_edges[e2].add(e1)
            self._new_out_edges[e1].add(e2)

        if _TIME:
            self._time_add_edge += time.clock() - t1

    def _has_edge(self, e1, e2):
        return e2 in self._out_edges[e1]

    def _add_last_entry(self):
        if self._gcirisnum % 1000 == 0:
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
            #     tmp = [e[0], e[0][0], e[0][1], e[1]]
            # else:
            #     tmp = [e[0], e[1]]
            #
            # for i in range(len(tmp)):
            #     if tmp[i] in self._double_entries:
            #         for j in range(i, len(tmp)):
            #             if tmp[j] in self._double_entries[tmp[i]]:
            #                 self._add_edge(e[0], (tmp[i],tmp[j]))
            # if type(e[0]) == tuple:
            #     for f in self._in_edges[e[0][0]] & self._in_edges[e[0][1]]:
            #         self._add_edge(f, e[0])

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
        self._update_node(e)


    def _update_node(self, ne):
        """
        An entry has been modified.
        """
        if _DEBUG:
            print("Updating the pile of " + str(ne))
        # self._merge_products(ne, e)

        newlinks = list()

        if _TIME:
            t1 = time.clock()

        cop = self._new_out_edges[ne].copy()
        self._new_out_edges[ne] = set()
        for x in cop:
            if x in self._double_entries:
                for y in self._double_entries[x] & self._out_edges[ne]:
                    tup = tuple(sorted((x,y)))
                    if tup not in self._out_edges[ne]:
                        self._add_edge(ne, tup)
                        for i in self._out_edges[tup]:
                            self._add_edge(ne, i)
                        for i in self._in_edges[ne]:
                            self._add_edge(i, tup)
                        newlinks.append(tup)

        if _TIME:
            self._time_lookups += time.clock() - t1
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
                c11 = treat(line[1][1])
                c12 = treat(line[1][2])
                self._add_concept(c11)
                self._add_concept(c12)
                c1 = tuple(sorted((c11, c12)))

                self._double_entries[c1[0]].add(c1[1])
            else:
                c1 = treat(line[1])
                self._add_concept(c1)
            c2 = treat(line[2])
            self._add_concept(c2)
            self._gcirisnum += 1
            self._gciris.append((c1, c2))
            self._add_last_entry()


if __name__ == "__main__":

    # TODO refactor tests

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
