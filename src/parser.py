# Copyright © 2021 Nils Seitz, Prof. Dr. Alexander Lischke

import os

import pandas as pd

from src.constants import ARGS as CONST
from src.constants import MODE
from src.tokens import Tokens


class Parser:
    # filters for defined FILETYPE_IN, saves to SAVE_PATH (see config file)
    # datapath is given bei notebook
    def __init__(self, datapath=CONST.DATA_PATH):
        self.filepaths = [os.path.join(datapath, file)
                          for *_, files in os.walk(datapath) for file in files
                          if file.endswith(CONST.FILETYPE_IN)]

        # check to exclude to accumulate file, so it does not accumulate itself
        # only create accumulated_df, if we actually accumulate
        if MODE in ['default', 'accumulate']:
            exclude = f'{CONST.FILENAME_ACCUM_DATA}.{CONST.FILETYPE_IN}'
            self.filepaths = [path for path in self.filepaths
                              if not path.endswith(exclude)]
            self.accumulated_df = pd.DataFrame()

    # reading in, processing and saving as FILETYPE_OUT
    # adding data points to accumulated_df and saving again in the end
    # savepath is given bei notebook
    def run(self, savepath=CONST.SAVE_PATH):
        # PHASE 1
        if MODE in ['default', 'preprocess']:
            for filepath in self.filepaths:
                # File get split into Lines
                file_lines = self.lines_filepath(filepath)

                # Lines get split to Token (experiment, block, id, [data])
                tokens = Tokens(*file_lines)
                tokens.transform()  # All Data Manipulation happens internally
                tokens.save_as_csv(savepath)  # saves final formatted data

                # Optimization: Final data can immediately be accumulated
                # This saves time by not reading in the data again
                if MODE == 'default':
                    self.append_to_accumulated_df(tokens.final_df)

        # PHASE 2
        elif MODE == 'accumulate':
            # Data is already formatted, so just read in and accumulate
            for filepath in self.filepaths:
                # File gets read in to DataFrame immediately
                csv_df = pd.read_csv(filepath)
                self.append_to_accumulated_df(csv_df)  # concat both DataFrames

        if MODE in ['default', 'accumulate']:
            self.save_accumulated_df_as_csv(savepath)  # save accumulated data

    # STATIC FUNCTIONS ################################################
    # reads in all lines of a file for a given path, return them as List[str]
    @staticmethod
    def lines_filepath(filepath):
        with open(filepath, 'r') as f:
            lines = []
            line = f.readline()  # get first line, if there is any
            while line:  # runs as long as there are lines left
                lines.append(line.strip())  # strip removes "\n" at end
                line = f.readline()  # get next line
            return lines  # returns a list of all stripped lines

    # HELPER FUNCTIONS ################################################
    # Automatically appends the new data
    # Merges existing or add not yet existing columns
    def append_to_accumulated_df(self, token_df):
        self.accumulated_df = pd.concat([self.accumulated_df, token_df])

    # Fills empty values and rounds values before saving to savepath
    def save_accumulated_df_as_csv(self, savepath):
        filename = f'{CONST.FILENAME_ACCUM_DATA}.{CONST.FILETYPE_OUT}'
        final_savepath = os.path.join(savepath, filename)

        # float_format -> all values have uniform decimal places (rounds, too)
        self.accumulated_df.to_csv(final_savepath,
                                   index=False,  # doesn't save index values
                                   float_format=f'%.{CONST.DECIMAL_PLACES}f')
