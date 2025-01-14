from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

map_a = {
    'A': ['B','E','D'],
    'B': 'AEC',
    'C': 'BED',
    'D': 'AEC',
    'E': 'ABCD',
}

map_b = {
    'A' : 'BED',
    'B' : 'AEC',
    'C' : 'BEF',
    'D' : 'AEF',
    'E' : 'ABCDF',
    'F' : 'CED',
}

map_c = {
    'A' : 'BFED',
    'B' : 'AFC',
    'C' : 'BFGD',
    'D' : 'AEGC',
    'E' : 'ADFG',
    'F' : 'ABCGDE',
}


def constraint(r1, c1, r2, c2):
    return c1 != c2

def make_constraint_graph(mapa):
    return { (X,Y): constraint for X in mapa for Y in mapa[X] }

def make_domains(reg, colo):
    return {r: colors for r in region}

cs = ConstraintSearch(make_domains(region, colors), make_constraint_graph(map_a))

print(cs.search())
