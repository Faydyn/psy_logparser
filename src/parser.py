# Copyright © 2021 Nils Seitz, Prof. Dr. Alexander Lischke
import os

import pandas as pd

from src.constants import ARGS as CONST
from src.constants import MODE
from src.tokens import Tokens


class Parser:

    # filters for .txt (default filetype input), saves to path specified in constants.json
    # datapath can also be overwritten if it is set in main.py
    def __init__(self, datapath=CONST.DATA_PATH):
        self.filepaths = [os.path.join(datapath, file)
                          for *_, files in os.walk(datapath) for file in files
                          if file.endswith(CONST.FILETYPE_IN)]

        if MODE in ['default', 'accumulate']:
            self.accum_filename = f'{CONST.FILENAME_ACCUM_DATA}.{CONST.FILETYPE_IN}'
            self.filepaths = [path for path in self.filepaths
                              if not path.endswith(self.accum_filename)]
            self.accum_filename = f'{CONST.FILENAME_ACCUM_DATA}.{CONST.FILETYPE_OUT}'
            self.accumulated_df = pd.DataFrame()

    # transformation and saving to .csv for each file, adding data to accum df
    def run(self, savepath=CONST.SAVE_PATH):
        if MODE in ['default', 'preprocess']:
            for filepath in self.filepaths:
                file_lines = self.lines_filepath(filepath)
                tokens = Tokens(*file_lines)
                tokens.transform()
                tokens.save_as_csv(
                    savepath)  # savepath can be overwritten, is optional arg

                if MODE == 'default':
                    self.append_to_accumulated_df(tokens.final_df)

        elif MODE == 'accumulate':
            for filepath in self.filepaths:
                csv_df = pd.read_csv(filepath)
                self.append_to_accumulated_df(csv_df)

        if MODE in ['default', 'accumulate']:
            self.save_accumulated_df_as_csv(savepath)

    def append_to_accumulated_df(self, token_df):
        self.accumulated_df = pd.concat([self.accumulated_df, token_df])

    def save_accumulated_df_as_csv(self, savepath):
        final_savepath = os.path.join(savepath, self.accum_filename)

        self.accumulated_df = self.accumulated_df.fillna(0)
        self.accumulated_df.to_csv(final_savepath,
                                   index=False,
                                   float_format=f'%.{CONST.DECIMAL_PLACES}f')

    # reads in all lines of a file for a given path to a list
    @staticmethod
    def lines_filepath(filepath):
        with open(filepath, 'r') as f:
            lines = []
            while line := f.readline():
                lines.append(line.strip())
            return lines
