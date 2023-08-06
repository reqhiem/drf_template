import pandas as pd
import os
current_file = os.path.abspath(os.path.dirname(__file__))


def get_by_year(
    year: int,
):
    df_2021 = pd.read_csv(os.path.join(current_file, 'data/2021.csv'))
    results = df_2021.head(5).to_dict('records')
    return results
