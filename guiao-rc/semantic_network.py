import dataclasses
from collections import Counter
from statistics import fmean


# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

class AssocNum(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)

class AssocOne(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None, rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) 
                and (rel_type == None or isinstance(d.relation, rel_type)) ]
        return self.query_result
    
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):
        assoc = self.query_local(rel_type=Association)
        return {a.relation.name for a in assoc}

    def list_objects(self):
        obj = self.query_local(rel_type=Member)
        return {o.relation.entity1 for o in obj}
    
    def list_users(self):
        users = {d.user for d in self.declarations}
        return users
    
    def list_types(self):

        types = set()
        for d in self.declarations:
            if isinstance(d.relation, (Member, Subtype)):
                types.add(d.relation.entity2)
                if isinstance(d.relation, Subtype):
                    types.add(d.relation.entity1)
        return types

    def list_local_associations(self, obj):
        assoc = self.query_local(rel_type=Association, e1=obj)
        return {a.relation.name for a in assoc}

    def list_relations_by_user(self, user):
        rels = self.query_local(user=user)
        return {r.relation.name for r in rels}
    
    def associations_by_user(self, user):
        assoc = self.query_local(user=user, rel_type=Association)
        assoc_names = {a.relation.name for a in assoc}
        return len(assoc_names)
    
    def list_local_associations_by_entity(self, entity):
        assoc = self.query_local(e1=entity, rel_type=Association)
        return {(a.relation.name, a.user) for a in assoc}

    def predecessor(self, a, b):

        # 1. listar todas as declaracoes de subtipos e membros
        types = self.query_local(rel_type=Subtype)
        members = self.query_local(rel_type=Member)

        # 2. procurar uma declaracao direta que ligue b aa 
        for m in members:
            if m.relation.entity1 == b and m.relation.entity2 == a:
                return True

        for t in types:
            if t.relation.entity1 == b and t.relation.entity2 == a:
                return True

        # 3. Se não houver uma ligação direta
        for t in types:
            if t.relation.entity1 == b:
                # Se b é um subtipo de algo
                if self.predecessor(a, t.relation.entity2):
                    return True

        for m in members:
            if m.relation.entity1 == b:
                # Se b é membro de algum tipo
                if self.predecessor(a, m.relation.entity2):
                    return True

        return False

    # this is dg's predecessor method
    def predecessor_dg(self,a ,b):
        local_predecessor = [d.relation.entity2 for d in self.query_local(e1=b, rel_type=(Member,Subtype))]
        if a in local_predecessor:
            return True
        
        return any([self.predecessor_dg(a, l) for l in local_predecessor])


    def predecessor_path(self, a, b):
        local_predecessor = [d.relation.entity2 for d in self.query_local(e1=b, rel_type=(Member,Subtype))]
        if a in local_predecessor:
            return [a,b]

        for path in [self.predecessor_path(a, l) for l in local_predecessor]:
            if path:
                return path + [b]

    def query(self, e, assoc=None):
        local_declarations = self.query_local(e1=e, rel=assoc, rel_type=Association)
        local_predecessors = [d.relation.entity2 for d in self.query_local(e1= e, rel_type=(Member, Subtype))]

        for p in local_predecessors:
            local_declarations.extend(self.query(p, assoc))

        return local_declarations

    def query2(self, e, assoc=None):
        local_declarations = self.query_local(e1=e, rel=assoc)
        local_predecessor = [d.relation.entity2 for d in self.query_local(e1= e, rel_type=(Member, Subtype))]

        for p in local_predecessor:
            local_declarations.extend(self.query(p, assoc))

        return local_declarations

    def query_cancel(self, e, assoc=None):
        # Primeiro, verifidar associações diretamente declaradas na entidade 'e'
        local_declarations = self.query_local(e1=e, rel=assoc, rel_type=Association)

        # Extraímos os nomes das associações diretamente ligadas à entidade 'e'
        local_assoc = {d.relation.name for d in local_declarations}

        # Buscar predecessores (membros e subtipos)
        local_predecessors = [d.relation.entity2 for d in self.query_local(e1=e, rel_type=(Member, Subtype))]

        # Iterar pelos predecessores para buscar associações, mas apenas se elas
        # não estiverem diretamente declaradas em 'e'
        for p in local_predecessors:
            inherited_decls = self.query_cancel(p, assoc)
            filtered_inherited_decls = [decl for decl in inherited_decls if decl.relation.name not in local_assoc]
            local_declarations.extend(filtered_inherited_decls)

        return local_declarations

    def query_down(self, e, assoc=None, first=True):
        local_declarations = [] if first else self.query_local(e1=e, rel=assoc)

        local_descent = [
            d.relation.entity1 for d in self.query_local(e2=e, rel_type=(Member, Subtype))
        ]

        for d in local_descent:
            local_declarations.extend(self.query_down(d, assoc, False))

        return local_declarations


    def query_induce(self, e, assoc = None):
        decl = self.query_down(e, assoc)

        # counter retorna uma lista de tuplas (elemento, frequência)
        return Counter([d.relation.entity2 for d in decl]).most_common(1)[0][0]


    def query_local_assoc(self, e, assoc):

        decl = self.query_local(e1=e, rel=assoc)
        hist = Counter([d.relation.entity2 for d in decl]).most_common()

        for d in decl:
            if isinstance(d.relation , AssocOne):
                v,t = hist[0]
                return v, t/len(decl)
            elif isinstance(d.relation, AssocNum):
                # fmean calcula a média de uma lista de números FAST
                # statistics é meta para o projeto
                return fmean([d.relation.entity2 for d in decl])
            elif isinstance(d.relation, Association):

                def lim_gen(assoc):
                    lim = 0
                    for a,f in assoc:
                        yield a,f
                        lim += f
                        if lim >= 0.75:
                            return

                    return list(lim_gen([(v,h/len(decl)) for v,h in hist]))

                lim = 0
                r = []
                for v,f in [(v,h/len(decl)) for v,h in hist]:
                    lim += f
                    r.append((v,f))
                    if lim >= 0.5:
                        return r

        return None



    def query_assoc_value(self, e, assoc):
        local_decl = self.query_local(e1=e, rel=assoc)

        local_hist =  Counter([d.relation.entity2 for d in local_decl]).most_common()
        if local_hist and local_hist[0][1] == len(local_decl): # primeira aliniea
            return local_hist[0][0]

        inher_decl = [ h for h in self.query(e, assoc) if h not in local_decl]

        inher_hist = Counter([d.relation.entity2 for d in inher_decl]).most_common()

        if not local_decl:
            return inher_hist[0][0]
        if not inher_decl:
            return local_hist[0][0]

        f = {v: t for v,t in local_hist}
        for v,f in inher_decl:
            f[v] = f.get(v,0) + f

        return sorted(f.items(), key=lambda x: -x[1])[0]