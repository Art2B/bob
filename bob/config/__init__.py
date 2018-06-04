import json
from os.path import abspath, dirname, join

config_path = join(dirname(abspath(__file__)), 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

def get():
    return config