categories_ = ["act", "Hotel", "fast_food", "Resto", "church", "camping", "museum", "nature", "tasting", "castle",
               "park", "gite", "sport"]

mixed = {'accommodation': [("Hotel", 0.33), ("camping", 0.33), ("gite", 0.34)],
          'food': [("fast_food", 0.2), ("Resto", 0.6), ("park", 0.2)],
          'activity': [("church", 0.125), ("museum", 0.125), ("nature", 0.125), ("tasting", 0.125), ("castle", 0.125), ("park", 0.125), ("sport", 0.125), ("act", 0.125)],
          'nighttime': [("act", 1.0)]}

fetard = {'accommodation': [("Hotel", 0.2), ("camping", 0.6), ("gite", 0.2)],
          'food': [("fast_food", 0.3), ("Resto", 0.4), ("park", 0.3)],
          'activity': [("church", 0.05), ("museum", 0.05), ("nature", 0.1), ("tasting", 0.05), ("castle", 0.05), ("park", 0.1), ("sport", 0.1), ("act", 0.5)],
          'nighttime': [("act", 1.0)]}

culturel = {'accommodation': [("Hotel", 0.4), ("camping", 0.1), ("gite", 0.4)],
          'food': [("fast_food", 0.1), ("Resto", 0.8), ("park", 0.1)],
          'activity': [("church", 0.2), ("museum", 0.3), ("nature", 0.05), ("tasting", 0.05), ("castle", 0.25), ("park", 0.05), ("sport", 0.05), ("act", 0.05)],
          'nighttime': [("act", 1.0)]}

campeur = {'accommodation': [("Hotel", 0.0), ("camping", 1), ("gite", 0.0)],
          'food': [("fast_food", 0.4), ("Resto", 0.2), ("park", 0.4)],
          'activity': [("church", 0.05), ("museum", 0.125), ("nature", 0.125), ("tasting", 0.05), ("castle", 0.2), ("park", 0.2), ("sport", 0.125), ("act", 0.125)],
          'nighttime': [("act", 1.0)]}

jeunes = {'accommodation': [("Hotel", 0.3), ("camping", 0.2), ("gite", 0.5)],
          'food': [("fast_food", 0.2), ("Resto", 0.6), ("park", 0.2)],
          'activity': [("church", 0.05), ("museum", 0.125), ("nature", 0.2), ("tasting", 0.05), ("castle", 0.125), ("park", 0.2), ("sport", 0.125), ("act", 0.125)],
          'nighttime': [("act", 1.0)]}

gastronomie = {'accommodation': [("Hotel", 0.7), ("camping", 0.05), ("gite", 0.25)],
          'food': [("fast_food", 0.2), ("Resto", 0.6), ("park", 0.2)],
          'activity': [("church", 0.1), ("museum", 0.15), ("nature", 0.1), ("tasting", 0.3), ("castle", 0.15), ("park", 0.05), ("sport", 0.05), ("act", 0.1)],
          'nighttime': [("act", 1.0)]}


def get_types_and_probas(sub_profile):
    return [x[0] for x in sub_profile], [x[1] for x in sub_profile]