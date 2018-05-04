import json

def read_json_file(file):
    with open(file, 'r') as json_file:
        return json.load(json_file)

