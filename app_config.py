import json
ENVIRONMENT_PATH = './environment/config.json'

config = ''
with open(ENVIRONMENT_PATH,'r') as file:
    config = dict(json.loads(file.read()))