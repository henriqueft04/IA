bn = [("C", [("A", True), ("B", True)], 0.95), ("C", [("A", True), ("B",
False)], 0.7), ("C", [("A", False), ("B", True)], 0.65), ("C", [("A",
False), ("B", False)], 0.1), ("D", [("C", True)], 0,77), ("D", [("C",
False)], 0,22), ("B", [], 0,33)]

def get_ancestors(bn, var):
    parents = []

    # Encontrar os pais diretos da variável
    for v in bn:
        if v[0] == var:
            parents += [x[0] for x in v[1]]

    # Eliminar duplicados
    parents = list(set(parents))

    # Buscar ancestrais recursivamente
    ancestors = parents[:]
    for parent in parents:
        ancestors += get_ancestors(bn, parent)

    return list(set(ancestors))


print(get_ancestors(bn, "D"))
    
