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
from graphs import datatourisme_hist, datatourisme_theme, chain, all_successors, all_predecessors, degeneralize, display
from dis_and_sim import halkidi, mval_sim, wu_palmer
import concurrent.futures



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


def build_instance_sequence(base_seq, instance_map, start_node_swap="Hotel"):
    if start_node_swap is not None:
        base_seq[0] = start_node_swap

    # Hotel is drawn once
    # numpy.random.choice
    hotel = choice(instance_map["Hotel"], 1)[0]

    outseq = []
    for item in base_seq:
        if item == "Hotel" or item == "Sleep":
            outseq.append(hotel)
        else:
            # numpy.random.choice
            outseq.append(choice(instance_map[item], 1)[0])

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
    return mval_sim(x, y, [datatourisme_main, datatourisme_theme, datatourisme_hist])


if __name__ == '__main__':


    # Instances
    data_instances = pd.read_csv(INSTANCES_FILE)
    hotels = data_instances[data_instances["category"] == "Hotel"]
    restos = data_instances[data_instances["category"] == "Resto"]
    activities = data_instances[data_instances["category"] == "act"]

    instances = {
        "Resto": list(map(lambda x: x[2], restos.values)),
        "act_matin": list(map(lambda x: x[2], activities.values)),
        "act_aprem": list(map(lambda x: x[2], activities.values)),
        "Hotel": list(map(lambda x: x[2], hotels.values)),
        "act_nocturne": list(map(lambda x: x[2], activities.values))}

    """## Display"""

    # display(datatourisme_theme, "datatourisme_theme.html", width="70%", height="600px")
    # display(datatourisme_hist, "datatourisme_hist.html", width='80%')
    # display(datatourisme_main, "datatourisme_main.html", width='80%')

    """# Demo"""

    seqs = []
    for i in range(1000):
        base = build_basic_sequence(chain, "Start", "Sleep")
        ids = build_instance_sequence(base, instances)
        mv = map_to_multival(ids, data_instances)
        seqs.append(mv)

    print("Writing", len(seqs), "sequences to", SEQ_FILE)
    with open(SEQ_FILE, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        spamwriter.writerow(["seq_id", "item_id", "main_tags", "event_tags", "archi_tags"])

        for seq_id, seq in enumerate(seqs):
            for item_id, item in enumerate(seq):
                line = [seq_id, item_id, ";".join(item[0]), ";".join(item[1]), ";".join(item[2])]
                spamwriter.writerow(line)




    print("Computing distance matrix")
    # Convert to numpy data type
    msize = int((len(seqs) * (len(seqs) - 1)) / 2) # Compute triangular matrix size
    np_seqs = []
    for seq in seqs:
        seqA = np.empty((len(seq),), dtype=object)
        for k in range(len(seq)):
            seqA[k] = seq[k]
        np_seqs.append(seqA)
    del seqs#Free memory

    ed = np.empty(msize, dtype=np.float32)
    idx = [(i, j) for i in range(1, len(np_seqs)) for j in range(1, i + 1)]

    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        future_to_coordinates = {executor.submit(ced, np_seqs[i], np_seqs[j], sim, gaussian): (i, j) for i in range(1, len(np_seqs)) for j in range(1, i + 1)}

        for future in concurrent.futures.as_completed(future_to_coordinates):
            coo = future_to_coordinates[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (coo, exc))
            else:
                ed[idx.index(coo)] = data


    """
    ed = np.empty(msize, dtype=np.float32)
    pos = 0
    for i in range(1, len(seqs)):
        for j in range(1, i + 1):
            ed[pos] = ced(np_seqs[i], np_seqs[j], sim, gaussian)
            pos += 1
    """
    np.savetxt("data/dis_matrix.txt", ed)

    #lk = linkage(ed, "ward")
    #dendo = dendrogram(lk)
    #plt.show()
