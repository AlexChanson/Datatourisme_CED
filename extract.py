import json
import os
from pprint import pprint
import csv

DATA_PATH = "./data/"
HEADER = ['label', "tags", "uri", "category", "theme", "architecture"]
CAT = [("Accommodation", "Hotel"), ("Restaurant", "Resto")]


def to_keep(tag):
    if tag == "PointOfInterest":
        return False
    if tag.startswith("schema:"):
        return False
    if tag.startswith("olo:"):
        return False
    return True


if __name__ == '__main__':
    archi_domain = []

    with open(DATA_PATH + "index.json") as idx:
        index = json.load(idx)

    # Parse each file, one entry per file
    entries = []
    for item in index:
        with open(DATA_PATH + "objects/" + item["file"]) as file:
            data = json.load(file)

        # Seperate hotel/restaurants from the rest
        type = "act"
        for tag in data["@type"]:
            if tag == "Accommodation":
                type = "Hotel"
                break
            if tag == "Restaurant":
                type = "Resto"
                break

        themes = []
        archi = []
        try:
            for theme in data["hasTheme"]:
                themes.extend(theme["@type"])
                #print(theme["@type"])
                if 'ArchitecturalStyle' in theme["@type"]:
                    archi.extend(theme["rdfs:label"]["fr"])
        except KeyError:
            pass
        archi_domain.extend(archi)

        #Cleanup
        tag_data = filter(to_keep, data["@type"])

        #Build entry
        entry = [item['label'], ";".join(tag_data), data["@id"][len("https://data.datatourisme.gouv.fr/"):], type, ";".join(themes), ";".join(archi)]
        entries.append(entry)

    with open(DATA_PATH + 'output.csv', 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',  quotechar='"', quoting=csv.QUOTE_ALL)
        spamwriter.writerow(HEADER)
        for line in entries:
            spamwriter.writerow(line)

    print("Active domain for architecture")
    print(set(archi_domain))
