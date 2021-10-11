import os

import pandas as pd

class Tokens:
    def __init__(self, exp, category, vpn, *data):
        def get_value(token):  # removes the "keyword"
            return token.split(':')[1].strip()

        #  transforms the lines into a proper Pandas DataFrame
        def file_lines_to_df(file_lines):
            separat_lines = [line.split('\t') for line in file_lines]  # Tabs
            col_name , *data_lines = separat_lines
            trial = col_name[0]  # name of the index row
            
            # make the format right with col_name and set_index
            df: pd.DataFrame = pd.DataFrame(data_lines,columns=col_name)
            df = df.set_index(trial)
            
            # 
            

            print(df.dtypes)
            return df


        self.experiment = get_value(exp)
        self.block = get_value(category)
        self.id = get_value(vpn)
        self.df: pd.DataFrame = file_lines_to_df(file_lines=data)



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
    def run(self,savepath):
        for filepath in self.filepaths:
            file_lines = self.lines_filepath(filepath)
            tokens = Tokens(*file_lines)
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
