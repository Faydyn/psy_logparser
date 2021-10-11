import os

from typing import List

import numpy as np


class Parser:

    # filters for .txt, saves RELATIVE path to root given
    def __init__(self, path_rootdir: str):
        for root, _, file in os.walk(path_rootdir):
            self.filepaths: List[str] = [os.path.join(root, f) for f in file if
                                         f.endswith('.txt')]

    # for debugging purposes
    def __str__(self) -> str:
        return self.filepaths.__str__()

    # transformation and saving to .csv for each file
    def run(self):
        for filepath in self.filepaths:
            tokenized = self.transform(self.lines_filepath(filepath))
            print(tokenized)
            break

    # reads in all lines of a file for a given path to a list
    def lines_filepath(self, filepath: str) -> List[str]:
        with open(filepath, 'r') as f:
            lines = []
            while line := f.readline():
                lines.append(line.strip())
            return lines

    def transform(self, file_lines: List[str]):
        return file_lines
