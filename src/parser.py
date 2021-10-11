import os

from src.tokens import Tokens


class Parser:
    # filters for .txt, saves RELATIVE path to root given
    def __init__(self, path_rootdir):
        self.root = os.path.abspath(path_rootdir)
        for _, _, file in os.walk(self.root):
            self.filepaths = [os.path.join(self.root, f) for f in file if
                              f.endswith('.txt')]
            self.filepaths.sort()

    # transformation and saving to .csv for each file
    def run(self, path_savedir):
        savedir = os.path.abspath(path_savedir)
        for filepath in self.filepaths:
            file_lines = self.lines_filepath(filepath)

            tokens = Tokens(*file_lines)
            tokens.transform_df()
            tokens.df.to_csv(os.path.join(savedir,f'{tokens.block}{tokens.id}.csv'))

    # reads in all lines of a file for a given path to a list
    @staticmethod
    def lines_filepath(filepath):
        with open(filepath, 'r') as f:
            lines = []
            while line := f.readline():
                lines.append(line.strip())
            return lines
