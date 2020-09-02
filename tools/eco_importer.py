import json

class EcoImporter:


    def get_ecos(self, filepath):
        openings = []
        with open(filepath) as json_file:
            data = json.load(json_file)
            for eco in data:
                openings.append((eco['name'], eco['eco'], eco['moves']))

        return openings
