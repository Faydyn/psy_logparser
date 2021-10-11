import os

from dataclasses import dataclass
import pandas as pd


# Simulates the structure from the example

@dataclass(repr=True,eq=True)
class Tokens:
    def __init__(self, exp, category, vpn, *data):
        def get_value(token):  # removes the "keyword"
            return token.split(':')[1].strip()

        def convert_block(category):
            # MAGIC CONSTANTS (SEE EXAMPLE TAB11)
            gono = {'TGT': 'go', 'NTGT': 'no'}
            emo = {'NEUTRAL': 'neu', 'HAPPY': 'hap', 'AFRAID': 'fea'}
            # "TGT NEUTRAL, NTGT HAPPY" -> "go_neu_no_hap"
            fst, snd = [x.strip().split(' ') for x in category.split(', ')]
            gn0, emo0 = fst
            gn1, emo1 = snd
            return f'{gono[gn0]}_{emo[emo0]}_{gono[gn1]}_{emo[emo1]}'

        # transforms the lines into a proper Pandas DataFrame
        def file_lines_to_df(file_lines):
            separat_lines = [line.split('\t') for line in file_lines]  # Tabs
            col_name, *data_lines = separat_lines
            trial, pic, rt, rs = col_name  # name of the index row
            # make the format right with col_name and set_index
            df = pd.DataFrame(data_lines, columns=col_name, dtype="string")
            df = df.set_index(trial)
            # change types to int64 with numerics
            df[rt] = pd.to_numeric(df[rt])
            df[rs] = pd.to_numeric(df[rs])
            return df

        self.experiment = get_value(exp)
        self.block = convert_block(get_value(category))
        self.id = get_value(vpn)
        self.df = file_lines_to_df(file_lines=data)

    def __str__(self):
        return self.__repr__()



class Parser:

    # filters for .txt, saves RELATIVE path to root given
    def __init__(self, path_rootdir):
        for root, _, file in os.walk(path_rootdir):
            self.filepaths = [os.path.join(root, f) for f in file if
                              f.endswith('.txt')]

    # for debugging purposes
    def __str__(self):
        return self.filepaths.__str__()

    # transformation and saving to .csv for each file
    def run(self, path_savedir):
        for filepath in self.filepaths:
            file_lines = self.lines_filepath(filepath)
            tokens = Tokens(*file_lines)
            print(tokens)
            break  # TODO: DEBUG BREAK POINT

    # reads in all lines of a file for a given path to a list
    def lines_filepath(self, filepath):
        with open(filepath, 'r') as f:
            lines = []
            while line := f.readline():
                lines.append(line.strip())
            return lines

    def transform(self, file_lines):
        return file_lines
