import json
import os

MODE = 'default'
__JSON_FILENAME = 'constants.json'


class Args:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


with open(os.path.abspath(__JSON_FILENAME)) as f:
    ARGS = Args(**json.load(f)[MODE])
