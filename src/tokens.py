from dataclasses import dataclass

import pandas as pd


# Simulates the structure from the example
@dataclass(repr=True, eq=True)
class Tokens:
    def __init__(self, exp, category, vpn, *data):
        self.TRIAL, self.PICTURE, self.RT, self.RS = ['trl', 'pic', 'rt', 'rs']
        self.emo_gn = {}

        def get_value(token):  # removes the "keyword"
            return token.split(':')[1].strip()

        def convert_block(category):
            # MAGIC CONSTANTS (SEE EXAMPLE TAB11)
            GONO = {'TGT': 'go', 'NTGT': 'no'}
            EMO = {'NEUTRAL': 'neu', 'HAPPY': 'hap', 'AFRAID': 'fea',
                   'ANGER': 'ans'}
            # TODO: ANGER IS NOT DEFINED BY CONVENTION (shortcut for it)
            # "TGT NEUTRAL, NTGT HAPPY" -> "go_neu_no_hap"
            fst, snd = [x.strip().split(' ') for x in category.split(', ')]
            gn0, emo0 = fst
            gn1, emo1 = snd
            # Sets Emotion to Go/NoGo, because its needed for transform_pic()
            self.emo_gn[EMO[emo0]] = GONO[gn0]
            self.emo_gn[EMO[emo1]] = GONO[gn1]

            return f'{GONO[gn0]}_{EMO[emo0]}_{GONO[gn1]}_{EMO[emo1]} '

        # transforms the lines into a proper Pandas DataFrame
        def file_lines_to_df(file_lines):
            sep_lines = [line.split('\t') for line in file_lines]  # Tabs
            # make the format right with col_name and set_index
            col_names = [self.TRIAL, self.PICTURE, self.RT, self.RS]
            df = pd.DataFrame(sep_lines[1:], columns=col_names, dtype="string")
            df = df.set_index(self.TRIAL)
            # change types to int64 with numerics
            df[self.RT] = pd.to_numeric(df[self.RT])
            df[self.RS] = pd.to_numeric(df[self.RS])
            return df

        self.experiment = get_value(exp)
        self.id = get_value(vpn)
        self.block = convert_block(get_value(category))
        self.df = file_lines_to_df(file_lines=data)

    def transform_df(self):
        self.transform_pic()

    def transform_pic(self):
        # MAGIC CONSTANT (SEE EXAMPLE TAB6)
        EMO = {'nes': 'neu', 'has': 'hap', 'afs': 'fea', 'ans': 'ans'}

        # TODO: ans(ANGER???) IS NOT DEFINED BY CONVENTION (shortcut for it)
        def clean_transf(cell):
            stripped = cell[8:-4].lower()  # clean: Set_T\GAF14NES.jpg -> f14nes
            sex, *num = stripped[:-3]  # first three chars
            emotion = stripped[-3:]
            emo = EMO[emotion]
            # gets go/no for the given emotion for this token (from block)
            gono = self.emo_gn[emo]
            return f'{sex}_{"".join(num)}_{emo}_{gono}'

        self.df[self.PICTURE] = self.df[self.PICTURE].apply(clean_transf)
        print(self.df)
