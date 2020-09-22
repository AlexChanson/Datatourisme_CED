from graphs import chain_culture, chain_fetard, chain_campeur, chain_jeunes

categories_ = ["act", "Hotel", "fast_food", "Resto", "church", "camping", "museum", "nature", "tasting", "castle",
               "park", "gite", "sport", "bar"]

mixed = {'accommodation': [("Hotel", 0.33), ("camping", 0.33), ("gite", 0.34)],
          'food': [("fast_food", 0.2), ("Resto", 0.6), ("park", 0.2)],
          'activity': [("church", 0.125), ("museum", 0.125), ("nature", 0.125), ("tasting", 0.125), ("castle", 0.125), ("park", 0.125), ("sport", 0.125), ("act", 0.125)],
          'nighttime': [("act", 0.1), ("bar", 0.9)],
         'name': 'mixed'}

fetard = {'accommodation': [("Hotel", 0.2), ("camping", 0.6), ("gite", 0.2)],
          'food': [("fast_food", 0.3), ("Resto", 0.4), ("park", 0.3)],
          'activity': [("church", 0.05), ("museum", 0.05), ("nature", 0.1), ("tasting", 0.05), ("castle", 0.05), ("park", 0.1), ("sport", 0.1), ("bar", 0.5)],
          'nighttime': [("act", 0.1), ("bar", 0.9)],
         'name': 'fetard', "chain": chain_fetard}

culturel = {'accommodation': [("Hotel", 0.4), ("camping", 0.2), ("gite", 0.4)],
          'food': [("fast_food", 0.1), ("Resto", 0.8), ("park", 0.1)],
          'activity': [("church", 0.2), ("museum", 0.3), ("nature", 0.05), ("tasting", 0.05), ("castle", 0.25), ("park", 0.05), ("sport", 0.05), ("act", 0.05)],
          'nighttime': [("act", 0.9), ("bar", 0.1)],
         'name': 'culturel', "chain": chain_culture}

campeur = {'accommodation': [("Hotel", 0.0), ("camping", 1), ("gite", 0.0)],
          'food': [("fast_food", 0.4), ("Resto", 0.2), ("park", 0.4)],
          'activity': [("church", 0.05), ("museum", 0.125), ("nature", 0.125), ("tasting", 0.05), ("castle", 0.2), ("park", 0.2), ("sport", 0.125), ("act", 0.125)],
          'nighttime': [("act", 0.1), ("bar", 0.9)],
         'name': 'campeur', "chain": chain_campeur}

jeunes = {'accommodation': [("Hotel", 0.3), ("camping", 0.2), ("gite", 0.5)],
          'food': [("fast_food", 0.2), ("Resto", 0.6), ("park", 0.2)],
          'activity': [("church", 0.05), ("museum", 0.125), ("nature", 0.2), ("tasting", 0.05), ("castle", 0.125), ("park", 0.2), ("sport", 0.125), ("act", 0.125)],
          'nighttime': [("act", 0.1), ("bar", 0.9)],
          'name': "jeunes", "chain": chain_jeunes}

gastronomie = {'accommodation': [("Hotel", 0.7), ("camping", 0.05), ("gite", 0.25)],
          'food': [("fast_food", 0.2), ("Resto", 0.6), ("park", 0.2)],
          'activity': [("church", 0.1), ("museum", 0.15), ("nature", 0.1), ("tasting", 0.3), ("castle", 0.15), ("park", 0.05), ("sport", 0.05), ("act", 0.1)],
          'nighttime': [("act", 0.1), ("bar", 0.9)],
         'name': 'gastronomie', "chain": chain_culture}


def get_types_and_probas(sub_profile):
    return [x[0] for x in sub_profile], [x[1] for x in sub_profile]


if __name__ == '__main__':
    print('-- Accommodation ---')
    print('accommodation,Hotel,Camping,Gite')
    for profile in [fetard, culturel, campeur, jeunes, gastronomie]:
        line = [profile["name"]]
        for t, p in profile["accommodation"]:
            line.append(str(p))
        print(",".join(line))
    print("--- Food ---")
    print("food,fast_food,resto,picknick")
    for profile in [fetard, culturel, campeur, jeunes, gastronomie]:
        line = [profile["name"]]
        for t, p in profile["food"]:
            line.append(str(p))
        print(",".join(line))
    print("--- Activity ---")
    print("activity,church,museum,nature,tasting,castle,park,sport,act")
    for profile in [fetard, culturel, campeur, jeunes, gastronomie]:
        line = [profile["name"]]
        for t, p in profile["activity"]:
            line.append(str(p))
        print(",".join(line))