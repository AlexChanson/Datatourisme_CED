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
from graphs import datatourisme_hist, datatourisme_theme, chain_fetard, all_successors, all_predecessors, degeneralize, display
from dis_and_sim import halkidi, mval_sim, wu_palmer, mval_sim_ignore_null
import concurrent.futures
import multiprocessing as mp



# Load data
ID_PREFIX = "https://data.datatourisme.gouv.fr/"  # Ids (URI) have been striped for memory/ease of use
INSTANCES_FILE = "data/output.csv"
ONTOLOGY_FILE = "data/graph"
SEQ_FILE = "data/seqs.csv"


"""## Model Vis"""
# Display code - Markov model
# display(chain, "markov.html", size_dynamic=False, height="600px", width="70%")


"""## Sequence Gen"""
def build_basic_sequence(markov, start_node, end_node, append_end_node=True):
    def white_walker(acc):
        successors = markov.successors(acc[-1])
        probas = []
        items = []
        for next in successors:
            items.append(next)
            probas.append(markov.get_edge_data(acc[-1], next)["weight"])
        # numpy.random.choice
        draw = choice(items, 1, p=probas)[0]

        if draw == end_node:
            if append_end_node:
                acc.append(draw)
            return acc

        acc.append(draw)
        return white_walker(acc)

    return white_walker([start_node])


def build_instance_sequence(base_seq, instance_map, profile, start_node_swap="Hotel"):
    if start_node_swap is not None:
        base_seq[0] = start_node_swap

    # Hotel is drawn once
    # numpy.random.choice
    acc_types, acc_probas = get_types_and_probas(profile["accommodation"])
    acc_type = choice(acc_types, 1, p=acc_probas)[0]
    hotel = choice(instance_map[acc_type], 1)[0]

    outseq = []
    for item in base_seq:
        if item == "Hotel" or item == "Sleep":
            outseq.append(hotel)
        elif item == "Resto":
            res_types, res_probas = get_types_and_probas(profile["food"])
            res_type = choice(res_types, 1, p=res_probas)[0]
            outseq.append(choice(instance_map[res_type], 1)[0])
        elif item == "act_matin" or item == "act_aprem":
            act_types, act_probas = get_types_and_probas(profile["activity"])
            act_type = choice(act_types, 1, p=act_probas)[0]
            outseq.append(choice(instance_map[act_type], 1)[0])
        else:
            act_type = "act"
            outseq.append(choice(instance_map[act_type], 1)[0])

    return outseq


def map_to_multival(seq, database):
    sem = []
    for item in seq:
        data = database[database["uri"] == item]
        tags = data["tags"].tolist()
        theme = data["theme"].tolist()
        archi = data["architecture"].tolist()
        sem_item = (set() if tags == [np.nan] else degeneralize(set(tags[0].split(';')), datatourisme_main),
                    set() if theme == [np.nan] else set(theme[0].split(';')),
                    set() if archi == [np.nan] else set(archi[0].split(';')))
        sem.append(sem_item)
    return sem


# Ontologies
raw_onto = nx.read_gml(ONTOLOGY_FILE)
datatourisme_main = raw_onto


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

    el1 = [{"Castle", "ShowEvent", "VisualArtsEvent"}, {"SpatialEnvironmentTheme"}, {"Renaissance"}]
    el2 = [{"Castle", "ParkAndGarden"}, {"SpatialEnvironmentTheme"}, {"Roman"}]

    print(detail(el1, el2))
    print(detail(el2, el1))