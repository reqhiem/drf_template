import pandas as pd
import os

current_file = os.path.abspath(os.path.dirname(__file__))


def get_by_type(primary_types):
    results = []

    for primary_type in primary_types:
        filename = os.path.join(current_file, f"data/{primary_type}.csv")
        df = pd.read_csv(filename)

        results.extend(df.to_dict('records'))

    df = pd.DataFrame(results)

    df['Datefull'] = pd.to_datetime(df['Datefull'])

    df = df.sort_values(by='Datefull')

    # Agrupar por fecha y sumar los totales
    df['TOTALES'] = df.groupby('Date')['Count'].transform('sum')

    return df.head(10000)
