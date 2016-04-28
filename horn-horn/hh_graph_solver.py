"""
@file hh_graph_solver.py
@author André Schrottenloher

"""

import copy
import hh_util
import collections


class SimpleGraph:

    def __init__(self):
        self._nodes = set()
        self._successors = collections.defaultdict(set)
        self._predecessors = collections.defaultdict(set)

    def get_successors(self, entry):
        return self._successors(entry)

    def get_predecessors(self, entry):
        return self._predecessors(entry)

    def add_edge(self, e1, e2):
        if e1 not in self._nodes:
            self._nodes.add(e1)
            self._successors[e1] = [e1]
            self._predecessors[e1] = [e1]
        if e2 not in self._nodes:
            self._nodes.add(e2)
            self._predecessors[e2] = [e2]
        for e in self._predecessors[e1]:
            self.successors[e] |= self.successors[e2]
        for e in self._predecessors[e2]:
            self._predecessors[e] |= self.predecessors[e1]

    def has_edge(self, e1, e2):
        return e1 in self._predecessors[e2]

class SpecialGraph:

    def __init__(self):
        self._nb = 0
        self._entry_id_to_entry = dict()
        self._graph = SimpleGraph()

        self._entries_to_remaining_questions = collections.defaultdict(set)
        self._qnb = 0
        self._questions = dict()
        self._remaining_questions = set()


    def search_entry(self, lits):
        """
        Searches for an entry with this exact set of lits.
        """
        # to_link_with = []
        for e in self._entry_id_to_entry:
            if self._entry_id_to_entry[e] == lits:
                return True, e
            # if not lits.difference(self._entry_id_to_entry[e]):
            #     to_link_with.append(e)

        self._nb += 1
        self._entry_id_to_entry[self._nb] = lits
        return False, self._nb

    def _all_entries_that_contain(self, lits):
        """
        @param lits A set of literals
        @return All entries (nodes of the graph) such that their (extended) set
        of successors contain lits ; as a set.
        """
        # TODO improve
        for e in self._entry_id_to_entry:
            if not lits.difference(self._entry_id_to_entry[e]):
                yield e


    def add_edge(self, entries):
        """
        Adds an edge in the graph between two entries (tuple).

        The parameters have to be sets of literals.
        """
        (e1, e2) = entries


    def _all_entries_contained_in(self, lits):
        """
        @param lits A set of literals.
        @return All entries (nodes in the graph) that are contained in this set.
        """
        # TODO improve
        for e in self._entry_id_to_entry:
            # if this is empty
            if not self._entry_id_to_entry[e].difference(lits):
                yield e

    def does_imply(self, tup):
        """
        @param tup a 2-tuple of set of literals ; the second can contain any number of lits.
        @return true if lit is in the extended successors of an entry that is contained in lits
        """
        tmp = self._all_entries_that_contain(tup[0])
        for e in tmp:
            if not tup[1].difference(self._graph.get_successors(e)):
                return True
        return False

    def memorize_question(self, q):
        """
        @param q A question (in fact, a 2-tuple of sets of literals, the second contains only one)
        @return An id for this question
        """
        self._qnb += 1
        self._questions[self._qnb] = q
        self._remaining_questions.add(self._qnb)
        return self._qnb

    def pop_question(self):
        """
        Find a question whose answer is true.

        @return The id of this question, None if there are nothing left.
        """
        for q in self._remaining_questions:
            if self.does_imply(self._questions[q]):
                self._remaining_questions.remove(q)
                return q
        return None


class GraphSolver:

    def __init__(self):
        self._graph = SpecialGraph()
        # self._outer_units = dict()
        self._clauses_to_questions = collections.defaultdict(set)
        self._questions_to_clauses = collections.defaultdict()
        self._outer_clauses = dict()

    def input(self, oclauses):
        self._outer_clauses = list_to_dict( [o for o in oclauses if o is not None] )
        if _DEBUG:
            for c in self._outer_clauses:
                hh_util.check_oc(self._outer_clauses[c])
        for c in self._outer_clauses:
            if self._outer_clauses[c][1] == []:
                self._graph.add_edge(_clause_to_edge(self._outer_clauses[c][0]))
            else:
                for q in self._outer_clauses[c][1]:
                    qid = self._graph.memorize_question(_clause_to_edge(q))
                    self._clauses_to_questions[c].add(qid)
                    self._questions_to_clauses[qid] = c

    def _clause_to_edge(c):
        (a,b) = c
        if a == None:
            return (set(b), "FALSE")
        elif b == []:
            return ("TRUE", set(b))
        else:
            return (set((a)), set(b))

    def solve(self):
        if _DEBUG:
            print("Solving.")

        for u in hh_solver.get_units(self._outer_clauses):
            self._graph.add_edge(_clause_to_edge(self._outer_units[u]))

        qid = self._graph.pop_question()

        while qid is not None:

            if self._graph.does_imply("TRUE", "FALSE"):
                if _DEBUG:
                    print("========================")
                    print("Done solving. This is False.")
                return False

            c = self._questions_to_clauses(qid)
            self._clauses_to_questions[c].remove(qid)
            if not self._clauses_to_questions[c]):
                # empty set of questions
                if self._outer_clauses[c][0] is None:
                    if _DEBUG:
                        print("========================")
                        print("Done solving. This is False.")
                    return False
                else:
                    if _DEBUG:
                        print("There is a new (outer) unit : " + str(self._outer_clauses[c][0]))
                    self._graph.add_edge(_clause_to_edge(self._outer_clauses[c][0]))

            qid = self._graph.pop_question()


        if _DEBUG:
            print("========================")
            print("Done solving. This is True.")
        return True
