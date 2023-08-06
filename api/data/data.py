import pandas as pd
import os
current_file = os.path.abspath(os.path.dirname(__file__))


class Data:
    df_2021 = None

    def __init__(self):
        self.df_2021 = pd.read_csv(os.path.join(current_file, '2021.csv'))

    def get_df_2021(self):
        return self.df_2021
