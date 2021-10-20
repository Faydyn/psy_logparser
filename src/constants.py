import json
import os

MODE = 'accumulate'
__JSON_FILENAME = 'constants.json'


class Args:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        # user defined Args from constants combined
        if MODE in ['default', 'preprocess']:
            self.BLOCK_ID = [self.TARGET_BLOCK,
                             self.TARGET_ID]
            self.RT_RS = [self.TARGET_RT,
                          self.TARGET_RS]
            self.TARGET_COLNAMES = [self.TARGET_TRIAL,
                                    self.TARGET_PICTURE,
                                    self.TARGET_RT,
                                    self.TARGET_RS]
            self.MATCH_DICT_FOR_KEY = [self.OLD_GONO_TO_TARGET,
                                       self.OLD_EMO_TO_TARGET] * 2

            # Static Values to access gono_emo_combi_block spefific for each block
            self.GONO_0 = 'GONO_0'
            self.GONO_1 = 'GONO_1'
            self.EMO_0 = 'EMO_0'
            self.EMO_1 = 'EMO_1'
            self.KEYS_BLOCK = [self.GONO_0, self.EMO_0, self.GONO_1, self.EMO_1]


with open(os.path.join(os.path.abspath('.'), __JSON_FILENAME)) as f:
    ARGS = Args(**json.load(f)[MODE])
