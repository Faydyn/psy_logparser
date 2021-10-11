import os

from typing import List

import numpy as np


class Parser:

    # filters for .txt, saves RELATIVE path to root given
    def __init__(self, path_rootdir: str):
        for root, _, file in os.walk(path_rootdir):
            self.filepaths: np.ndarray = np.array([os.path.join(root, f) for f in file if
                                         f.endswith('.txt')])

    def __str__(self) -> str:
        return self.filepaths.__str__()
