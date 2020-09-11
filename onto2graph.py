from onto2nx import OWLParser, parse_owl
import networkx as nx
import pickle

parser = OWLParser(file="./data/onto_xml.owl")
print("Parsed OWL file")

outgraph = nx.DiGraph()

for n in parser.nodes():
    outgraph.add_node(n)
for u, v in parser.edges():
    if u != v:
        outgraph.add_edge(u, v)

components = nx.weakly_connected_components(outgraph)
to_keep = set()

for comp in components:
    if "PlaceOfInterest" in comp:
        to_keep.update(comp)
to_del = set(outgraph.nodes()).difference(to_keep)

outgraph.remove_nodes_from(to_del)
outgraph = outgraph.reverse()
outgraph = nx.relabel_nodes(outgraph, {"PointOfInterest": "All"})

# Flip equivalent edges
pseudo_roots = []
for node in outgraph:
    if len(nx.ancestors(outgraph, node)) == 0 and node != "All":
        pseudo_roots.append(node)

for u, v in nx.edges(outgraph, pseudo_roots):
    print("Flipped", u, "->", v)
    outgraph.remove_edge(u, v)
    outgraph.add_edge(v, u)

nx.write_gml(outgraph, "./data/graph")