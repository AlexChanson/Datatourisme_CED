"""
    Alexandre Chanson
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from numpy.random import choice
from scipy.cluster.hierarchy import dendrogram, linkage
import csv

from CED import *
from Context_function import gaussian
from graphs import datatourisme_hist, chain_fetard, all_successors, all_predecessors, degeneralize, display
from dis_and_sim import halkidi, mval_sim, wu_palmer, mval_sim_ignore_null
import concurrent.futures
import multiprocessing as mp



# Load data
ID_PREFIX = "https://data.datatourisme.gouv.fr/"  # Ids (URI) have been striped for memory/ease of use
INSTANCES_FILE = "data/output.csv"
ONTOLOGY_FILE = "data/graph_main.gml"
SEQ_FILE = "data/seqs.csv"


# Ontologies
datatourisme_main = nx.read_gml(ONTOLOGY_FILE)
datatourisme_theme = nx.read_gml("./data/graph_event.gml")


def sim(x, y):
    return mval_sim_ignore_null(x, y, [datatourisme_main, datatourisme_theme, datatourisme_hist])


if __name__ == '__main__':
    from profiles import *
    # Instances
    data_instances = pd.read_csv(INSTANCES_FILE)
    instances = dict()
    for cat in categories_:
        instances[cat] = list(data_instances[data_instances["category"] == cat]["uri"])

    from dis_and_sim import halkidi, wu_palmer

    def detail(s, s_, onts=[datatourisme_main, datatourisme_theme, datatourisme_hist]):
        items = []
        for i, ont in enumerate(onts):
            items.append(halkidi(s[i], s_[i], wu_palmer, ont))

        return items

    def sim(x, y):
        return mval_sim_ignore_null(x, y, [datatourisme_main, datatourisme_theme, datatourisme_hist])


    s1 = [[{"CamperVanArea"}, {}, {}], [{"GroupLodging"}, {}, {}], [{"ParkAndGarden"}, {}, {}],
          [{"CamperVanArea"}, {}, {}], [{"CamperVanArea"}, {}, {}], [{"CamperVanArea"}, {}, {}]]
    s2 = [[{"CamperVanArea"}, {}, {}], [{"FastFoodRestaurant"}, {}, {}], [{"CamperVanArea"}, {}, {}],
          [{"CamperVanArea"}, {}, {}], [{"FastFoodRestaurant"}, {}, {}], [{"CamperVanArea"}, {}, {}]]

    sa = np.empty((len(s1),), dtype=object)
    sb = np.empty((len(s1),), dtype=object)

    for i in range(len(s1)):
        sa[i] = s1[i]
    for i in range(len(s2)):
        sb[i] = s2[i]

    print(ced(sa, sb, sim, gaussian))


"""
el1 = [{"Castle", "ShowEvent", "VisualArtsEvent"}, {"SpatialEnvironmentTheme"}, {"Renaissance"}]
el2 = [{"Castle", "ParkAndGarden"}, {"SpatialEnvironmentTheme"}, {"Roman"}]
el3 = [{"Product", "Tasting", "WineCellar"}, {"SpatialEnvironmentTheme"}, {}]
el4 = [{"Guesthouse"}, {}, {}]

print("el1,el2", detail(el1, el2))
print("el1,el3", detail(el1, el3))
print("el2,el3", detail(el2, el3))
print("el1,el4", detail(el2, el3))
print("el2,el4", detail(el2, el3))
print("el3,el4", detail(el2, el3))
print("--- --- ---")
print("halkidi Cinema Cliff", halkidi({"Cinema"}, {"Cliff"}, wu_palmer, datatourisme_main))
print("halkidi Cinema Mine", halkidi({"Cinema"}, {"Mine"}, wu_palmer, datatourisme_main))
"""



