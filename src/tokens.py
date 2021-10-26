# Copyright © 2021 Nils Seitz, Prof. Dr. Alexander Lischke

import os

import numpy as np
import pandas as pd

from src.constants import ARGS as CONST


def load_user_defined_constants():  # user defined Args from constants combined
    CONST.BLOCK_ID = [CONST.TARGET_BLOCK,
                      CONST.TARGET_ID]
    CONST.RT_RS = [CONST.TARGET_RT,
                   CONST.TARGET_RS]
    CONST.TARGET_COLNAMES = [CONST.TARGET_TRIAL,
                             CONST.TARGET_PICTURE,
                             CONST.TARGET_RT,
                             CONST.TARGET_RS]
    CONST.MATCH_DICT_FOR_KEY = [CONST.OLD_GONO_TO_TARGET,  # GoNo,Emo,GoNo,Emo
                                CONST.OLD_EMO_TO_TARGET] * 2

    # Constants to access gono_emo_combi_block (Dict) specific for each block
    CONST.GONO_0 = 'GONO_0'
    CONST.GONO_1 = 'GONO_1'
    CONST.EMO_0 = 'EMO_0'
    CONST.EMO_1 = 'EMO_1'
    CONST.KEYS_BLOCK = [CONST.GONO_0, CONST.EMO_0, CONST.GONO_1, CONST.EMO_1]


class Tokens:
    load_user_defined_constants()  # statically load additional constants

    def __init__(self, exp, category, vpn, *data):  # * means "everything else"
        self.gono_emo_combi_block = {}  # Order of GoNo/Emo for this block
        self.emo_to_gono_block = {}  # Assignment Emo : GoNo for this block.
        self.experiment = self.get_value(exp)  # "FAC-EMO-GO-II-B-P-2"
        self.id = self.get_value(vpn)  # "HR24.02.84"
        self.block = self.get_value(category)  # "go_neu_no_hap" after methods
        self.df = self.create_df(data)  # Lines of a file parsed to DataFrame
        self.final_df = pd.DataFrame()  # Formatted DF, gets filled in the end

    # For debugging purposes
    def __str__(self):
        return f'''
Experiment: {self.experiment}
Block: {self.block}
id: {self.id}
{self.df.__str__()}'''

    # Pipeline for Data Manipulation, steps are explained inside functions
    def transform(self):
        self.split_block()
        self.convert_block()
        self.set_emo_to_gono()
        self.transform_picture_col()
        self.create_final_df()
        self.fill_final_df()

    # Fills empty values and rounds values before saving to savepath
    def save_as_csv(self, savepath):
        filename = f'{self.block}{self.id}.{CONST.FILETYPE_OUT}'
        final_savepath = os.path.join(savepath, filename)

        # float_format -> all values have uniform decimal places (rounds, too)
        self.final_df.to_csv(final_savepath,
                             index=False,  # doesn't save index values
                             float_format=f'%.{CONST.DECIMAL_PLACES}f')

    # STATIC FUNCTIONS ################################################
    @staticmethod
    def get_value(key_value):  # removes the "key" and strips value
        # "id: NS11.11.88" -> " NS11.11.88" -> "NS11.11.88"
        _, value = key_value.split(':')
        return value.strip()

    # transforms the lines of a file into a proper Pandas DataFrame
    @staticmethod
    def create_df(data):
        # data points in file lines are separated by tabs
        data_matrix = [line.split('\t') for line in data]  # "\t" = Tab

        # Drop the first row with [1:] (column names)
        # Replace with the defined column names from constant
        df = pd.DataFrame(data_matrix[1:], columns=CONST.TARGET_COLNAMES)

        # Replace the default index with the Trial number
        df = df.set_index(CONST.TARGET_TRIAL)

        # change types to int with numerics because we do math on these cols
        df[CONST.TARGET_RT] = pd.to_numeric(df[CONST.TARGET_RT])
        df[CONST.TARGET_RS] = pd.to_numeric(df[CONST.TARGET_RS])

        return df

    # HELPER FUNCTIONS #################################################
    # Sets up the GoNo or Emo (with respect to order) found in block
    def set_gono_emo_combi_block(self, values):  # {gn0 : "TGT", ...}
        self.gono_emo_combi_block = dict(zip(CONST.KEYS_BLOCK, values))

    # PRIVATE FUNCTIONS ################################################
    def split_block(self):  # preprocesses block data for convert_block
        gono_emo_pairs = [x.strip().split(' ') for x in self.block.split(', ')]
        gono_emo_combi = [x for gono_emo in gono_emo_pairs for x in gono_emo]
        self.set_gono_emo_combi_block(values=gono_emo_combi)
        # "TGT NEUTRAL, NTGT HAPPY" -> "TGT NEUTRAL" "NTGT HAPPY" ->
        # "TGT" "NEUTRAL" "NTGT" "HAPPY" -> {gn0 : "TGT", ..., emo1 : "HAPPY"}

    # Converts each old GoNo/Emo to new GoNo/Emo according to definition
    # {gn0 : "TGT", ..., emo1 : "HAPPY"} -> {gn0 : "go", ..., emo1 : "hap"}
    def convert_block(self):
        block_data = []
        for KEY, convert in zip(CONST.KEYS_BLOCK, CONST.MATCH_DICT_FOR_KEY):
            old_gono_or_emo_block = self.gono_emo_combi_block[KEY]
            converted_gono_or_emo_block = convert[old_gono_or_emo_block]
            block_data.append(converted_gono_or_emo_block)  # ["go",...,"hap"]

        # update with new terms since we need them later
        self.set_gono_emo_combi_block(values=block_data)

        # concat in order from left to right with "_" in between = "block"
        self.block = '_'.join(block_data)  # OUTPUT: "go_neu_no_hap"

    # Used For transform_picture_col(): Take Emo from the picture_id and
    # match with corresponding GoNo because that "pair" is defined in block
    # Only do after convert_block(), so we got transformed Emo/GoNo to pair
    def set_emo_to_gono(self):
        def set_dict_emo_to_gono_block(key_emo_block, key_gono_block):
            emo_block = self.gono_emo_combi_block[key_emo_block]
            gono_block = self.gono_emo_combi_block[key_gono_block]
            self.emo_to_gono_block[emo_block] = gono_block

        set_dict_emo_to_gono_block(CONST.EMO_0, CONST.GONO_0)  # neu : go
        set_dict_emo_to_gono_block(CONST.EMO_1, CONST.GONO_1)  # hap : no

    def transform_picture_col(self):
        def clean_transform(cell):
            # "Set_T\GAF14NES.jpg" -> "f14nes", care with Minus sign for LAST
            stripped = cell[CONST.TARGET_PICTURENAME_REMOVE_FIRST:
                            -CONST.TARGET_PICTURENAME_REMOVE_LAST].lower()

            # first 3 chars ("f14", sex = "f", num = ["1", "4"])
            sex, *num = stripped[:CONST.TARGET_PICTURENAME_SPLIT_SEXNUM_AFTER]

            # after first 3 (emo = "nes"), convert (as defined in constants)
            emo = stripped[CONST.TARGET_PICTURENAME_SPLIT_SEXNUM_AFTER:]
            target_emo = CONST.OLD_EMO_SHORT_TO_TARGET[emo]  # "nes" -> "neu"

            # Gets GoNo for the given Emo for this token block
            gono = self.emo_to_gono_block[target_emo]

            # num is List, it has to be joined (with nothing in between (""))
            return f'{sex}_{"".join(num)}_{emo}_{gono}'

        # Each cell in the picture column gets processed by clean_transform()
        self.df[CONST.TARGET_PICTURE] = \
            self.df[CONST.TARGET_PICTURE].apply(clean_transform)

    def create_final_df(self):  # Only doable with converted block name
        # All possible combinations of "go_neu_no_hap_[hi/mi/fa/cr]_[rt/rs]"
        final_colnames = [f'{self.block}_{mode}_{r}'
                          for mode in CONST.FINAL_COLNAMES
                          for r in CONST.RT_RS]
        all_colnames = CONST.BLOCK_ID + final_colnames  # adds "block","id"

        # Initializes blank DataFrame with according columns/column names
        self.final_df = pd.DataFrame(np.zeros((1, 16)), columns=all_colnames)

    # Filter and calculation
    def fill_final_df(self):
        # WARNING: set_value_final_df() uses Namespace of fill_final_df(),
        # meaning that it doesn't get filter_df passed in, but uses THE SAME.
        # DO NOT assign a new variable "filter_df" inside set_value_final_df()!
        def set_value_final_df(sig_name):
            # "go_neu_no_hap_[hi/mi/fa/cr]_rt"/"go_neu_no_hap_[hi/mi/fa/cr]_rs"
            rt = f'{self.block}_{sig_name}_{CONST.TARGET_RT}'
            rs = f'{self.block}_{sig_name}_{CONST.TARGET_RS}'

            # Mean for RT, leaves empty for empty filter_df.
            # If not empty!: Count for RS, cast to float for consistency
            self.final_df[rt] = filter_df[CONST.TARGET_RT].mean()
            count = len(filter_df[CONST.TARGET_RT])
            self.final_df[rs] = float(count) if count else np.nan

        # block and id stay identical
        self.final_df[CONST.TARGET_BLOCK] = self.block  # df["block"] = <block>
        self.final_df[CONST.TARGET_ID] = self.id  # df["id"] = <id>

        # first calculate the 4 signal columns (hi/mi/fa/cr)
        for sig in CONST.SIG_COLNAMES:
            filter_df = self.df[  # Filters for Go/No depending on signal
                self.df[CONST.TARGET_PICTURE].str.endswith(
                    CONST.SIGNAL_TO_GONO[sig])]
            filter_df = filter_df[  # Filters for 0/1 == RS (dep. on signal)
                filter_df[CONST.TARGET_RS] == CONST.SIGNAL_TO_RS_VALUE[sig]]
            set_value_final_df(sig_name=sig)

            # om = mi, co = fa
            # if sig is "mi"/"fa" it copies the values for "om"/"fa"
            nonsig = CONST.SIG_EQUIVALENT_NONSIG.get(sig)
            if nonsig:
                set_value_final_df(sig_name=nonsig)

        # Just add up the values of "om" and "fa" for RT and RS to get "er"
        for nonsig in CONST.NONSIG_COLNAMES:  # calculate er = om + co
            for r in CONST.RT_RS:
                comb_colname = f'{self.block}_{CONST.NONSIG_COMBINED}_{r}'
                nonsig_colname = f'{self.block}_{nonsig}_{r}'
                self.final_df[comb_colname] += self.final_df[nonsig_colname]
