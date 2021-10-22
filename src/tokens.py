# Copyright © 2021 Nils Seitz, Prof. Dr. Alexander Lischke


import os

import numpy as np
import pandas as pd

from src.constants import ARGS as CONST

# user defined Args from constants combined
CONST.BLOCK_ID = [CONST.TARGET_BLOCK,
                  CONST.TARGET_ID]
CONST.RT_RS = [CONST.TARGET_RT,
               CONST.TARGET_RS]
CONST.TARGET_COLNAMES = [CONST.TARGET_TRIAL,
                         CONST.TARGET_PICTURE,
                         CONST.TARGET_RT,
                         CONST.TARGET_RS]
CONST.MATCH_DICT_FOR_KEY = [CONST.OLD_GONO_TO_TARGET,
                            CONST.OLD_EMO_TO_TARGET] * 2

# Static Values to access gono_emo_combi_block specific for each block
CONST.GONO_0 = 'GONO_0'
CONST.GONO_1 = 'GONO_1'
CONST.EMO_0 = 'EMO_0'
CONST.EMO_1 = 'EMO_1'
CONST.KEYS_BLOCK = [CONST.GONO_0, CONST.EMO_0, CONST.GONO_1, CONST.EMO_1]


class Tokens:

    def __init__(self, exp, category, vpn, *data):

        self.gono_emo_combi_block = {}  # Dict of Order GoNo/Emo in Block
        self.emo_to_gono_block = {}
        self.experiment = self.get_value(exp)
        self.id = self.get_value(vpn)
        self.block = self.get_value(category)
        self.df = self.create_df(data)
        self.final_df = pd.DataFrame()

    # For debugging purposes
    def __str__(self):
        return f'''
Experiment: {self.experiment}
Block: {self.block}
id: {self.id}
{self.df.__str__()}'''

    def transform(self):
        self.split_block()
        self.convert_block()
        self.set_emo_to_gn()
        self.transform_picture_col()
        self.create_final_df()
        self.fill_final_df()

    def save_as_csv(self, savedir):
        filename = f'{self.block}{self.id}.{CONST.FILETYPE_OUT}'
        full_savepath = os.path.join(savedir, filename)

        self.final_df = self.final_df.fillna(CONST.FILL_EMPTY_WITH)
        self.final_df = self.final_df.round(CONST.DECIMAL_PLACES)
        self.final_df.to_csv(full_savepath,
                             index=False,
                             float_format=f'%.{CONST.DECIMAL_PLACES}f')

    # STATIC FUNCTIONS FOR INIT ########################################
    @staticmethod
    def get_value(key_value):  # removes the "keyword"
        _, value = key_value.split(':')
        return value.strip()

    # transforms the lines into a proper Pandas DataFrame
    @staticmethod
    def create_df(data):
        data_matrix = [line.split('\t') for line in data]  # Tabs

        #  Drop colnames and replace with constant and set_index to trial
        df = pd.DataFrame(data_matrix[1:], columns=CONST.TARGET_COLNAMES)
        df = df.set_index(CONST.TARGET_TRIAL)

        # change types to int with numerics
        df[CONST.TARGET_RT] = pd.to_numeric(df[CONST.TARGET_RT])
        df[CONST.TARGET_RS] = pd.to_numeric(df[CONST.TARGET_RS])
        return df

    # HELPER FUNCTIONS #################################################
    def set_gono_emo_combi_block(self, values):
        self.gono_emo_combi_block = dict(zip(CONST.KEYS_BLOCK, values))

    # PRIVATE FUNCTIONS ################################################

    def split_block(self):  # INPUT: "TGT NEUTRAL, NTGT HAPPY"
        gono_emo_pairs = [x.strip().split(' ') for x in self.block.split(', ')]
        gono_emo_combi = [x for gono_emo in gono_emo_pairs for x in gono_emo]
        self.set_gono_emo_combi_block(values=gono_emo_combi)
        # OUTPUT: { gn0 : "TGT", .. , emo1 : "HAPPY" }

    def convert_block(self):
        block_data = []
        for KEY, convert in zip(CONST.KEYS_BLOCK, CONST.MATCH_DICT_FOR_KEY):
            gono_or_emo_block = self.gono_emo_combi_block[KEY]
            converted_gono_or_emo_block = convert[gono_or_emo_block]
            block_data.append(converted_gono_or_emo_block)

        self.set_gono_emo_combi_block(values=block_data)  # update w/ new terms
        self.block = '_'.join(block_data)  # OUTPUT: "go_neu_no_hap"

    def set_emo_to_gn(self):
        def set_dict_emo_to_gono_block(emo, gono):
            emo_block = self.gono_emo_combi_block[emo]
            gono_block = self.gono_emo_combi_block[gono]
            self.emo_to_gono_block[emo_block] = gono_block

        set_dict_emo_to_gono_block(CONST.EMO_0, CONST.GONO_0)
        set_dict_emo_to_gono_block(CONST.EMO_1, CONST.GONO_1)

    def transform_picture_col(self):
        def clean_transform(cell):
            # Clean: Set_T\GAF14NES.jpg -> f14nes
            stripped = cell[CONST.TARGET_PICTURENAME_REMOVE_FIRST:
                            -CONST.TARGET_PICTURENAME_REMOVE_LAST].lower()
            # first three chars
            sex, *num = stripped[:CONST.TARGET_PICTURENAME_SPLIT_SEXNUM_AFTER]
            # other chars than first 3
            emo = stripped[CONST.TARGET_PICTURENAME_SPLIT_SEXNUM_AFTER:]
            target_emo = CONST.OLD_EMO_SHORT_TO_TARGET[emo]
            # gets GoNo for the given emotion for this token block
            gono = self.emo_to_gono_block[target_emo]
            return f'{sex}_{"".join(num)}_{emo}_{gono}'

        # noinspection PyTupleItemAssignment
        self.df[CONST.TARGET_PICTURE] = \
            self.df[CONST.TARGET_PICTURE].apply(clean_transform)

    def create_final_df(self):
        final_colnames = [f'{self.block}_{mode}_{r}'
                          for mode in CONST.FINAL_COLNAMES
                          for r in CONST.RT_RS]
        all_colnames = CONST.BLOCK_ID + final_colnames
        self.final_df = pd.DataFrame(np.zeros((1, 16)), columns=all_colnames)

    def fill_final_df(self):
        def set_value_final_df(sig_name):
            colname_rt = f'{self.block}_{sig_name}_{CONST.TARGET_RT}'
            colname_rs = f'{self.block}_{sig_name}_{CONST.TARGET_RS}'

            self.final_df[colname_rt] = filter_df[CONST.TARGET_RT].mean()
            self.final_df[colname_rs] = float(len(filter_df[CONST.TARGET_RS]))

        self.final_df[CONST.TARGET_BLOCK] = self.block
        self.final_df[CONST.TARGET_ID] = self.id

        for sig in CONST.SIG_COLNAMES:
            filter_df = self.df[  # Filters for Go/No
                self.df[CONST.TARGET_PICTURE].str.endswith(
                    CONST.SIGNAL_TO_GONO[sig])]
            filter_df = filter_df[  # Filters for 0/1 == RS
                filter_df[CONST.TARGET_RS] == CONST.SIGNAL_TO_RS_VALUE[sig]]
            set_value_final_df(sig_name=sig)

            # om = mi, co = fa
            if nonsig := CONST.SIG_EQUIVALENT_NONSIG.get(sig):
                set_value_final_df(sig_name=nonsig)

        for nonsig in CONST.NONSIG_COLNAMES:  # calculate er = om + co
            for r in CONST.RT_RS:
                comb_colname = f'{self.block}_{CONST.NONSIG_COMBINED}_{r}'
                nonsig_colname = f'{self.block}_{nonsig}_{r}'
                self.final_df[comb_colname] += self.final_df[nonsig_colname]
