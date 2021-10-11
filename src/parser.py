import os

from tokens import Tokens


class Parser:

    # filters for .txt, saves RELATIVE path to root given
    def __init__(self, path_rootdir):
        for root, _, file in os.walk(path_rootdir):
            self.filepaths = [os.path.join(root, f) for f in file if
                              f.endswith('.txt')]
            self.filepaths.sort()

    # for debugging purposes
    def __str__(self):
        return self.filepaths.__str__()

    # transformation and saving to .csv for each file
    def run(self, path_savedir):
        for filepath in self.filepaths:
            file_lines = self.lines_filepath(filepath)
            tokens = Tokens(*file_lines)
            tokens.transform_df()

    # reads in all lines of a file for a given path to a list
    def lines_filepath(self, filepath):
        with open(filepath, 'r') as f:
            lines = []
            while line := f.readline():
                lines.append(line.strip())
            return lines
