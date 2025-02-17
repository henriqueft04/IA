#encoding: utf8
import doctest
from itertools import product

# YOUR NAME: Henrique Ferreira Teixeira
# YOUR NUMBER: 114588

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):

from semantic_network import *
from constraintsearch import *
from bayes_net import *
from collections import Counter, defaultdict, deque


class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED

    # General query method, processing different types of
    # relations according to their specificities

    def query(self, entity, relname):
        all_decls = self.query_local(relname=relname)
        if not all_decls:
            return []

        # relaçoao mais comum
        type_count = Counter()
        for d in all_decls:
            if isinstance(d.relation, Member):
                type_count['Member'] += 1
            elif isinstance(d.relation, Subtype):
                type_count['Subtype'] += 1
            elif isinstance(d.relation, AssocOne):
                type_count['AssocOne'] += 1
            elif isinstance(d.relation, AssocSome):
                type_count['AssocSome'] += 1
            elif isinstance(d.relation, AssocNum):
                type_count['AssocNum'] += 1
            else:
                type_count['AssocSome'] += 1

        # Escolher o tipo mais comum
        chosen_type = type_count.most_common(1)[0][0]

        # mais facil
        def type_matches(rel):
            relation_type_map = {
                'Member': Member,
                'Subtype': Subtype,
                'AssocOne': AssocOne,
                'AssocSome': AssocSome,
                'AssocNum': AssocNum
            }
            return isinstance(rel, relation_type_map[chosen_type])

        #  guardar a ordem original porque estava a dar problemas
        if chosen_type in ['Member', 'Subtype']:
            result = []
            for d in self.declarations:
                if (d.relation.name == relname
                        and d.relation.entity1 == entity
                        and type_matches(d.relation)
                        and d.relation.entity2 not in result):
                    result.append(d.relation.entity2)
            return result

        ancestors_chain = [entity] + self.get_predecessors(entity)

        filtered_decls = [d for d in self.declarations
                          if d.relation.name == relname
                          and type_matches(d.relation)]

        if chosen_type == 'AssocSome':
            values_collected = []
            seen = set()
            for d in self.declarations:
                if (d.relation.name == relname
                        and type_matches(d.relation)
                        and d.relation.entity1 in ancestors_chain):
                    val = d.relation.entity2
                    if val not in seen:
                        seen.add(val)
                        values_collected.append(val)
            return values_collected

        for ent in ancestors_chain:
            local_vals = [d.relation.entity2 for d in filtered_decls if d.relation.entity1 == ent]
            if local_vals:
                if chosen_type == 'AssocOne':
                    return [Counter(local_vals).most_common(1)[0][0]]
                elif chosen_type == 'AssocNum':
                    return [sum(local_vals) / len(local_vals)]

        return []

    def get_predecessors(self, entity):
        predecessors = []
        current_parents = [d.relation.entity2 for d in self.query_local(e1=entity) if isinstance(d.relation, (Member, Subtype, Association))]
        for parent in current_parents:
            predecessors.append(parent)
            predecessors.extend(self.get_predecessors(parent))

        return list(dict.fromkeys(predecessors))


class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)

    def get_mothers(self, var):
        mothers = set()
        for (mt, mf, _) in self.dependencies.get(var, []):
            mothers.update(mt)
            mothers.update(mf)
        return mothers


    def get_ancestors(self, var):
        ancestors = set()
        to_visit = {var}
        visited = set()

        while to_visit:
            current = to_visit.pop()
            if current in visited:
                continue

            visited.add(current)
            moms = self.get_mothers(current)

            ancestors.update(moms)
            to_visit.update(moms)

        return ancestors

    def test_independence(self, v1, v2, given):
        # 1. variaveis relevantes
        relevant_vars = {v1, v2}.union(given)
        for var in list(relevant_vars):
            relevant_vars.update(self.get_ancestors(var))

        # 2. grafo
        edges = set()

        def add_edge(a, b):
            # facilitar logistica da drena
            if a != b:
                edge = tuple(sorted([a, b]))
                edges.add(edge)

        # ligá-los às mães 🫂
        for var in relevant_vars:
            moms = self.get_mothers(var)
            relevant_moms = moms.intersection(relevant_vars)

            for mom in relevant_moms:
                add_edge(var, mom)

            mom_list = list(relevant_moms)
            for i in range(len(mom_list)):
                for j in range(i + 1, len(mom_list)):
                    add_edge(mom_list[i], mom_list[j])

        edges = {e for e in edges if not set(e).intersection(given)}

        # 4. depth-first, se calhar há melhores opções, não o saberia dizer
        def has_path(start, end, graph):
            visited = set()

            def dfs(node):
                if node == end:
                    return True
                visited.add(node)
                for neighbor in (n for e in graph for n in e if node in e and n != node):
                    if neighbor not in visited:
                        if dfs(neighbor):
                            return True
                return False

            return dfs(start)

        is_independent = not has_path(v1, v2, edges)
        return list(edges), is_independent


class MyCS(ConstraintSearch):

    def __init__(self, domains, constraints):
        super().__init__(domains, constraints)

    def search_all(self, domains=None):
        if domains is None:
            domains = self.domains

        if any(len(d) == 0 for d in domains.values()):
            return []

        # se só houver um valor para cada variável, verificar se tá top
        if all(len(d) == 1 for d in domains.values()):
            assignment = {v: d[0] for v, d in domains.items()}
            for (v1, v2), constraint in self.constraints.items():
                if not constraint(v1, assignment[v1], v2, assignment[v2]):
                    return []

            return [assignment]

        # escolher variável com menos valores possíveis para dar branch
        var = min((v for v in domains if len(domains[v]) > 1), key=lambda x: len(domains[x]))

        all_solutions = []
        for val in domains[var]:
            new_domains = {v: d[:] for v, d in domains.items()}
            new_domains[var] = [val]

            self.propagate(new_domains, var)

            solutions = self.search_all(new_domains)
            all_solutions.extend(solutions)

        unique_solutions = []
        seen = set()
        for sol in all_solutions:
            tsol = tuple(sorted(sol.items()))
            if tsol not in seen:
                seen.add(tsol)
                unique_solutions.append(sol)

        return unique_solutions


def handle_ho_constraint(domains, constraints, variables, constraint):
    # Generate a unique auxiliary variable name
    base_aux_var = "aux_" + "_".join(variables)
    aux_var = base_aux_var
    counter = 1
    while aux_var in domains:
        aux_var = f"{base_aux_var}_{counter}"
        counter += 1

    from itertools import product
    var_domains = [domains[v] for v in variables]
    valid_tuples = [combo for combo in product(*var_domains) if constraint(combo)]

    domains[aux_var] = valid_tuples

    index_map = {v: i for i, v in enumerate(variables)}

    for v in variables:
        i = index_map[v]

        constraints[(aux_var, v)] = lambda nv, nv_val, vv, vv_val, i=i: nv_val[i] == vv_val

        constraints[(v, aux_var)] = lambda vv, vv_val, nv, nv_val, i=i: nv_val[i] == vv_val

    return aux_var