"""# Halkidi"""

import networkx as nx
from functools import lru_cache


@lru_cache(maxsize=100000)
def wu_palmer(x, y, Ontologie, rootnode="All"):
    return (2.0 * nx.shortest_path_length(Ontologie, rootnode, nx.lowest_common_ancestor(Ontologie, x, y))) / (
                nx.shortest_path_length(Ontologie, rootnode, x) + nx.shortest_path_length(Ontologie, rootnode, y))


# New stuff
def halkidi(X, Y, delta, ontology):
    if len(X) == 0 or len(Y) == 0:
        return 0
    return 1.0 / 2 * (
            1.0 / len(X) * sum(max(delta(x, y, ontology) for y in Y) for x in X) +
            1.0 / len(Y) * sum(max(delta(x, y, ontology) for x in X) for y in Y)
    )


def mval_sim(s, s_, onts):
    sum_ = 0
    for i, ont in enumerate(onts):
        sum_ += halkidi(s[i], s_[i], wu_palmer, ont)

    return sum_ / float(len(onts))