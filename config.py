import yaml

PATH = 'config.yml'

def get():
    with open(PATH) as file:
        return yaml.load(file, Loader=yaml.FullLoader)
    return {}
