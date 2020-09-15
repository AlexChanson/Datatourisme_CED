import networkx as nx
from pyvis.network import Network


datatourisme_theme = nx.DiGraph()
datatourisme_theme.add_node("SpatialEnvironmentTheme")
datatourisme_theme.add_edges_from([("All", "CulturalTheme"), ("All", "ParkAndGardenTheme"), ("All", "HealthTheme"),
                                   ("All", "FoodEstablishementTheme"), ("All", "FoodProduct"),
                                   ("All", "SpatialEnvironmentTheme"), ("All", "SportsTheme"),
                                   ("All", "EntertainmentAndEventTheme"), ("All", "CuisineCategory"),
                                   ("All", "RouteTheme"), ("RouteTheme", "CycleRouteTheme"),
                                   ("RouteTheme", "MTBRouteTheme"), ("All", "CommonAmenity")])


datatourisme_hist = nx.DiGraph()
datatourisme_hist.add_edges_from(
    [("All", "Médiéval"), ("Médiéval", "Gothique"), ("Médiéval", "Roman"), ("All", "Renaissance"),
     ("All", "Antiquité"), ("Antiquité", "Gallo-romain"), ("All", "XVII/XVIII"), ("XVII/XVIII", "Classique"),
     ("XVII/XVIII", "Néo-Classique"), ("All", "Moderne"), ("Moderne", "Contemporain"), ("Moderne", "Xixe siècle"),
     ("Moderne", "Xxe siècle")])


"""# Generator model"""

# Chaine de Markov
chain = nx.DiGraph()
r = "Resto"
m = "act_matin"
a = "act_aprem"
h = "Hotel"
s = "Sleep"
n = "act_nocturne"
st = "Start"
# Start
chain.add_edge(st, m, weight=0.7)
chain.add_edge(st, r, weight=0.2)
chain.add_edge(st, h, weight=0.1)
# Activité matin
chain.add_edge(m, m, weight=0.3)
chain.add_edge(m, r, weight=0.5)
chain.add_edge(m, a, weight=0.1)
chain.add_edge(m, h, weight=0.1)
# Resto
chain.add_edge(r, a, weight=0.8)
chain.add_edge(r, h, weight=0.1)
chain.add_edge(r, s, weight=0.1)
# Activité Aprem
chain.add_edge(a, a, weight=0.3)
chain.add_edge(a, h, weight=0.5)
chain.add_edge(a, n, weight=0.2)
# Hotel (Soir)
chain.add_edge(h, s, weight=0.75)
chain.add_edge(h, n, weight=0.25)
# Activité Nocturne
chain.add_edge(n, n, weight=0.1)
chain.add_edge(n, s, weight=0.9)


def all_successors(G, n, all_succ):
    all_succ += [n]
    for _n in G.successors(n):
        if _n not in all_succ:
            all_successors(G, _n, all_succ)
    return all_succ


def all_predecessors(Graph, node):
    def internal(G, n, acc):
        acc += [n]
        for _n in G.predecessors(n):
            if _n not in acc:
                internal(G, _n, acc)
        return acc

    return internal(Graph, node, [])

def degeneralize(concepts, ontology):
    more_general = set()

    for concept in concepts:
        to_rem = all_predecessors(ontology, concept)
        to_rem.remove(concept)

        more_general.update(to_rem)

    return concepts.difference(more_general)


def display(G, filename, size_dynamic=True, height='750px', width="100%", notebook=True):
    # pyvis.Network
    g = Network(height=height, width=width, directed=True, heading=filename.rstrip(".html"))

    if size_dynamic:
        size = lambda Graph, node: 80 * len(all_successors(Graph, node, []))
    else:
        size = lambda Graph, node: 80

    for n in G:
        if n == "Start":
            g.add_node(n, value=size(G, n), label=n, color="Green")
        elif n == "Sleep":
            g.add_node(n, value=size(G, n), label=n, color="Red")
        else:
            g.add_node(n, value=size(G, n), label=n, )
    for edge in G.edges:
        try:
            g.add_edge(edge[0], edge[1], label=G.get_edge_data(edge[0], edge[1])["weight"])
        except KeyError:
            g.add_edge(edge[0], edge[1])

    g.show_buttons(filter_=['physics'])
    g.show(filename)