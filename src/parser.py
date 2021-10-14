import os

from src.tokens import Tokens


class Parser:
    # filters for .txt, saves path to root given
    def __init__(self, path_datadir='data'):
        self.root = os.path.abspath('.')
        for root, _, file in os.walk(os.path.join(self.root, path_datadir)):
            self.filepaths = [os.path.join(root, f) for f in file if
                              f.endswith('.txt')]
            self.filepaths.sort()  # TODO: DEBUG

    # transformation and saving to .csv for each file
    def run(self, path_savedir='out'):
        savedir = os.path.join(self.root, path_savedir)
        for filepath in self.filepaths:
            file_lines = self.lines_filepath(filepath)

            tokens = Tokens(*file_lines)
            tokens.transform()
            tokens.save_as_csv(savedir)

    # reads in all lines of a file for a given path to a list
    @staticmethod
    def lines_filepath(filepath):
        with open(filepath, 'r') as f:
            lines = []
            while line := f.readline():
                lines.append(line.strip())
            return lines
