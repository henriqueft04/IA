

class BayesNet:

    def __init__(self, ldep=None):  # Why not ldep={}? See footnote 1.
        if not ldep:
            ldep = {}
        self.dependencies = ldep

    # The network data is stored in a dictionary that
    # associates the dependencies to each variable:
    # { v1:deps1, v2:deps2, ... }
    # These dependencies are themselves given
    # by another dictionary that associates conditional
    # probabilities to conjunctions of mother variables:
    # { mothers1:cp1, mothers2:cp2, ... }
    # The conjunctions are frozensets of pairs (mothervar,boolvalue)
    def add(self,var,mothers,prob):
        self.dependencies.setdefault(var,{})[frozenset(mothers)] = prob

    # Joint probability for a given conjunction of
    # all variables of the network
    def jointProb(self,conjunction):
        prob = 1.0
        for (var,val) in conjunction:
            for (mothers,p) in self.dependencies[var].items():
                if mothers.issubset(conjunction):
                    prob*=(p if val else 1-p)
        return prob

    def individualProb(self,var,val):

        # identity the independent variables
        # and the dependent variables
        indep = []
        dep = []
        for k in self.dependencies.keys():
            if len(self.dependencies[k]) == 0:
                indep.append(k)
            else:
                dep.append(k)

        # if the variable is independent
        # the probability is the one given
        # in the dictionary
        if var in indep:
            return self.dependencies[var]

        # if the variable is dependent
        # the probability is calculated
        # using the joint probability
        else:
            prob = 0
            for i in range(2**len(dep)):
                conj = []
                for j in range(len(dep)):
                    conj.append((dep[j],(i>>j)&1))
                prob += self.jointProb(conj)
            return



# Footnote 1:
# Default arguments are evaluated on function definition,
# not on function evaluation.
# This creates surprising behaviour when the default argument is mutable.
# See:
# http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments

