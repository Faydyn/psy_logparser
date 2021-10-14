import os

import numpy as np
import pandas as pd


# used Shortcuts: gn - Go/NoGo || emo - Emotion
# Simulates the structure from the example
class Tokens:
    # Static Variables / MAGIC CONSTANTS / Conventions from Example
    BLOCK, ID = BLOCK_ID = ['block', 'id']
    TRIAL, PICTURE, RT, RS = ['trl', 'pic', 'rt', 'rs']
    GO, NO = TARGET_GN = ['go', 'no']
    GONO = dict(zip(['TGT', 'NTGT'], TARGET_GN))  # S. TAB11
    __TARGET_EMO = ['neu', 'hap', 'fea', 'ang']
    EMO = dict(zip(['NEUTRAL', 'HAPPY', 'AFRAID', 'ANGER'], __TARGET_EMO))
    EMO_SHORT = dict(zip(['nes', 'has', 'afs', 'ans'], __TARGET_EMO))  # S. TAB6
    SIG_DETECT_MODES = ['hi', 'mi', 'fa', 'cr', 'er', 'co', 'om']
    AMOUNT_CALC_MODES = 4
    __CHECK_RESULTS = [(True, False), (False, False), (True, True), (False, True)]
    SIG_CHECKS = dict(zip(range(4), __CHECK_RESULTS))
    # 2 bool funcs to check - lambda x: 1. x.endswith('go'), 2. x == 0
    # can make dict for [hi,fa,mi,cr] with [(TF),(FF),(TT),(FT)]

    def __init__(self, exp, category, vpn, *data):
        def get_value(token):  # removes the "keyword"
            return token.split(':')[1].strip()

        self.gnemo_lst = []  # [gn0, emo0, gn1, emo1], filled in split_block()
        self.emo_gn = {}  # filled in set_emo_gn()
        self.experiment = get_value(exp)
        self.id = get_value(vpn)
        self.block = get_value(category)
        self.df = data  # is List[str] in this state
        self.final_df = 0  # filled in fill_final_df()

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
        self.set_emo_gn()
        self.preprocess_df()
        self.transform_picture_col()
        self.create_final_df()
        self.fill_final_df()

    def save_as_csv(self, savedir):
        self.final_df.to_csv(
            os.path.join(savedir, f'{self.block}{self.id}.csv'), index=False)

    # PRIVATE FUNCTIONS #################################################
    # needed for next 2 steps (convert_block and set_emotions)
    def split_block(self):  # splits data to gnemo_lst
        # "TGT NEUTRAL, NTGT HAPPY"
        nested_list = [x.strip().split(' ') for x in self.block.split(', ')]
        self.gnemo_lst = [x for sublist in nested_list for x in sublist]
        # [gn0, emo0, gn1, emo1] (needed for convert_block() and set_emo_gn())

    def convert_block(self):
        # -> "go_neu_no_hap"
        gn0, emo0, gn1, emo1 = self.gnemo_lst
        self.block = f'{self.GONO[gn0]}_{self.EMO[emo0]}_{self.GONO[gn1]}_{self.EMO[emo1]}'

    def set_emo_gn(self):
        # Sets Emotion to Go/NoGo, because its needed for transform_pic()
        def set_dict_emo_gn(emo, gn):
            self.emo_gn[self.EMO[emo]] = self.GONO[gn]

        gn0, emo0, gn1, emo1 = self.gnemo_lst
        set_dict_emo_gn(emo0, gn0)
        set_dict_emo_gn(emo1, gn1)

    # transforms the lines into a proper Pandas DataFrame
    def preprocess_df(self):
        sep_lines = [line.split('\t') for line in self.df]  # Tabs
        # make the format right with col_name and set_index
        col_names = [self.TRIAL, self.PICTURE, self.RT, self.RS]
        self.df = pd.DataFrame(sep_lines[1:], columns=col_names, dtype="string")
        self.df = self.df.set_index(self.TRIAL)
        # change types to int64 with numerics
        self.df[self.RT] = pd.to_numeric(self.df[self.RT])
        self.df[self.RS] = pd.to_numeric(self.df[self.RS])

    def transform_picture_col(self):
        def clean_transform(cell):
            stripped = cell[8:-4].lower()  # clean: Set_T\GAF14NES.jpg -> f14nes
            sex, *num = stripped[:3]  # first three chars
            emotion = stripped[3:]  # other chars than first 3
            emo = self.EMO_SHORT[emotion]
            # gets go/no for the given emotion for this token (from block)
            gn = self.emo_gn[emo]
            return f'{sex}_{"".join(num)}_{emo}_{gn}'

        self.df[self.PICTURE] = self.df[self.PICTURE].apply(clean_transform)

    def create_final_df(self):
        # ORDER MATTERS HERE
        final_colnames = [f'{self.block}_{mode}_{r}' for mode in
                          self.SIG_DETECT_MODES
                          for r in [self.RT, self.RS]]
        all_colnames = self.BLOCK_ID + final_colnames
        self.final_df = pd.DataFrame(np.zeros((1, 16), dtype=np.int32),
                                     columns=all_colnames)

    def fill_final_df(self):
        self.final_df[self.BLOCK] = self.block
        self.final_df[self.ID] = self.id

        for i, sig in enumerate(self.SIG_DETECT_MODES[:self.AMOUNT_CALC_MODES]):
            is_go, is_zero = self.SIG_CHECKS[i]  # get check results
            end = 'go' if is_go else 'no'
            gn_filter = self.df[self.df[self.PICTURE].str.endswith(end)]
            for r in [self.RT, self.RS]:
                # get the filtered data and sum it up / count it
                tmp_df = gn_filter[gn_filter[r] == 0 if is_zero else gn_filter[r] > 0]
                # TODO: WHAT if >0 or ==0, count or sum?
                self.final_df[f'{self.block}_{sig}_{r}'] = max(sum(tmp_df[r]),len(tmp_df))
                # max(sum,len) solves problem of summing 0's to 0 => len >= sum
                # There arent mixed 0 and non-0: If everything is not zero
                # (i. e. >= 1, since no floats) => sum >= len

