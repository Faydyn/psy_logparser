import os

from typing import List


class Parser:
    def __init__(self):
        self.filepaths: List[str] = []
        pass

    def read_in(self, path_rootdir: str) -> None:
        for root, _, file in os.walk(path_rootdir):
            self.filepaths = [os.path.join(root, f) for f in file if
                              f.endswith('.txt')]
