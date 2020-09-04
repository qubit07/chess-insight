import json
from opening import Opening

class OpeningImporter:


    def get_opening_systems(self, filepath):
        opening_systems = []
        with open(filepath) as json_file:
            data = json.load(json_file)
            for opening in data:
                family = opening['name'].split(',')[0]
                opening_systems.append(family)

        return set(opening_systems)

    def get_openings(self, filepath):
        openings = []
        with open(filepath) as json_file:
            data = json.load(json_file)
            for opening in data:
                family = opening['name'].split(',')[0]
                opening = Opening(opening['name'], opening['eco'], family, opening['moves'])
                openings.append(opening)

        return openings
