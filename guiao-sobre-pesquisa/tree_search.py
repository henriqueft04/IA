
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2020,
#  Inteligência Artificial, 2014-2023

from abc import ABC, abstractmethod
import math
# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        if all(pc in state for pc in action.pc):
            newstate = [s for s in state if s not in action.neg]
            newstate.extend(action.pos)

            return newstate
        return None

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        (x1,y1) = self.coordinates[state]
        (x2,y2) = self.coordinates[goal]
        return math.dist((x1,y1),(x2,y2))

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
        self.heuristic = domain.heuristic(initial,goal)
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,cost, heuristic=0): 
        self.state = state
        self.parent = parent
        self.depth = parent.depth + 1 if parent != None else 0
        self.cost = cost
        self.heuristic = heuristic
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)
    def in_parent(self,newstate):
        if self.parent == None:
            return False
        if self.parent.state == newstate:
            return True
        
        return self.parent.in_parent(newstate)


# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial,None,0, problem.heuristic)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None

        self.non_terminals = 0
        self.highest_cost_nodes = [root]
        self.average_depth = 0
        self.total_depth = 0

    @property
    def terminals(self):
        return len(self.open_nodes) + 1

    @property
    def avg_branching(self):
        return (self.non_terminals + self.terminals - 1)  / self.non_terminals if self.non_terminals > 0 else 0

    @property
    def length(self):
        return self.solution.depth 
    
    @property
    def cost(self):
        return self.solution.cost

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self, limit=None):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                return self.get_path(node)
            
            self.non_terminals += 1

            if limit is not None and node.depth >= limit:
                continue 

            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if node.in_parent(newstate):
                    continue

                cost = self.problem.domain.cost(node.state,a) + node.cost
                newnode = SearchNode(newstate,node,cost, self.problem.domain.heuristic(newstate, self.problem.goal))
                lnewnodes.append(newnode)
                self.total_depth += newnode.depth
                self.average_depth = self.total_depth / (self.non_terminals+self.terminals)
                if newnode.cost > self.highest_cost_nodes[0].cost:
                    self.highest_cost_nodes = [newnode]
                elif newnode.cost == self.highest_cost_nodes[0].cost:
                    self.highest_cost_nodes.append(newnode)

            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.cost + x.heuristic)

