# Copyright © 2021 Nils Seitz, Prof. Dr. Alexander Lischke

import json
import os

MODE = 'default'  # changed mode here
__JSON_FILEPATH = 'constants.json'  # change path to config file if wanted


class Args:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        # This makes sure, this classes variables are named like the keys
        # loaded from the json file and get corresponding values assigned


with open(os.path.abspath(__JSON_FILEPATH)) as f:
    ARGS = Args(**json.load(f)[MODE])  # Instantiate this class as global var

if not os.path.isdir(ARGS.SAVE_PATH):
    os.makedirs(ARGS.SAVE_PATH)
