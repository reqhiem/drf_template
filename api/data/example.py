import pandas as pd
import os

current_file = os.path.abspath(os.path.dirname(__file__))
df_2021 = pd.read_csv(os.path.join(current_file, '2021.csv'))

print(df_2021.head(5).to_dict('records'))
