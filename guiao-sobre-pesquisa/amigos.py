from constraintsearch import *
from mapas import constraint

amigos = ["Andre", "Bernardo", "Claudio"]

def constraint(a1,i1,a2,i2):
    b1, c1 = i1
    b2, c2 = i2

    if b1 == c1 or b2 == c2:
        return False # chapeu n é igual à bicla

    if a1 in i1 or a2 in i2:
        return False # nao posso levar as minhas coisas

    if (c1 == "Claudio" and b1 != "Bernardo") or (c2 == "Claudio" and b2 != "Bernardo"):
        return False

    return True


def make_constraint_graph(amigos):
    return {(X,Y): constraint for X in amigos for Y in amigos if X != Y}

def make_domains(amigos):
    return {A: [(B,C) for B in amigos for C in amigos] for A in amigos}

cs = ConstraintSearch(make_domains(amigos), make_constraint_graph(amigos))

print(cs.search())
