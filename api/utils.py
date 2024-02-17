import pandas as pd
from django.http import JsonResponse
# import matplotlib.pyplot as plt
import json
import os
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import numpy as np
from kneed import KneeLocator

current_file = os.path.abspath(os.path.dirname(__file__))


def get_type(primary_types):
    results = []

    for primary_type in primary_types:
        filename = os.path.join(current_file, f"data/{primary_type}.csv")

        # Utilizar la función chunksize para procesar por bloques
        chunk_size = 1000
        chunks = pd.read_csv(filename, chunksize=chunk_size)
        for chunk in chunks:
            chunk = chunk.dropna()

            # Convertir 'Datefull' directamente al formato datetime
            chunk['Datefull'] = pd.to_datetime(chunk['Datefull'])

            results.append(chunk)

    # Concatenar todos los DataFrames en uno solo
    df = pd.concat(results)

    # Ordenar el DataFrame por 'Datefull' después de la concatenación
    df = df.sort_values(by='Datefull')

    # Convertir DataFrame a lista de diccionarios
    data_dict_list = df.to_dict(orient='records')

    return data_dict_list


def get_by_type(primary_types):
    results = []

    for primary_type in primary_types:
        filename = os.path.join(current_file, f"data/{primary_type}.csv")
        df = pd.read_csv(filename)

        results.extend(df.to_dict('records'))

    df = pd.DataFrame(results)

    df['Datefull'] = pd.to_datetime(df['Datefull'])
    df = df[df['Datefull'].dt.year == 2010]

    df = df.sort_values(by='Datefull')

    # Agrupar por fecha y sumar los totales
    df['TOTALES'] = df.groupby('Date')['Count'].transform('sum')

    return df


def get_geojson():
    geojson_path = '/home/kate/Desktop/TesisFinal/chicago_Community_areas.geojson'

    with open(geojson_path) as geojson_file:
        geojson_data = json.load(geojson_file)

    return geojson_data


def get_comunity_areas():
    comunity_areas_path = '/home/kate/Desktop/TesisFinal/comunity_areas_names.csv'

    filename = pd.read_csv(comunity_areas_path)
    return filename


def get_clusters():
    Clusters_info = '/home/kate/Desktop/TesisFinal/test.csv'

    filename = pd.read_csv(Clusters_info)
    return filename


def get_info_dot_map():
    Dot_info = '/home/kate/Desktop/TesisFinal/Categorias/Fraude.csv'

    filename = pd.read_csv(Dot_info)
    return filename


def get_info_bar_polar():
    BarPolar_info = '/home/kate/Desktop/TesisFinal/BarPolar.csv'

    filename = pd.read_csv(BarPolar_info)
    return filename


def processDataForBarChart(categories, year):
    results = []
    for category in categories:
        file_path = f"/home/kate/Desktop/TesisFinal/Categorias/{category}.csv"

        df = pd.read_csv(file_path)

        if 'Original_Date' in df.columns:
            df['Original_Date'] = pd.to_datetime(df['Original_Date'])

            df_filtered = df[df['Original_Date'].dt.year == int(year)]

            df_filtered['Hour'] = df_filtered['Original_Date'].dt.hour

            all_hours_df = pd.DataFrame(index=range(24), columns=df_filtered['Primary_Type'].unique(), data=0)

            for crime_type, values in df_filtered.groupby('Primary_Type')['Hour'].value_counts().items():
                all_hours_df.loc[crime_type[1], crime_type[0]] = values

            index_values = list(all_hours_df.index)
            crime_types_info = [{'type': crime_type, 'values': list(all_hours_df[crime_type])} for crime_type in all_hours_df.columns]

            results.append({'category': category, 'index_values': index_values, 'crime_types_info': crime_types_info})

    return results


def processDataForMultiLineChart(categories, year):
    results = []
    for category in categories:
        file_path = f"/home/kate/Desktop/TesisFinal/Categorias/{category}.csv"

        df = pd.read_csv(file_path)

        if 'Original_Date' in df.columns:
            df['Original_Date'] = pd.to_datetime(df['Original_Date'])

            df_filtered = df[df['Original_Date'].dt.year == int(year)]

            df_filtered['Month'] = df_filtered['Original_Date'].dt.month_name()

            all_months_df = pd.DataFrame(index=df_filtered['Month'].unique(), columns=df_filtered['Primary_Type'].unique(), data=0)

            for crime_type, values in df_filtered.groupby(['Month', 'Primary_Type']).size().items():
                all_months_df.loc[crime_type[0], crime_type[1]] = values

            index_values = list(all_months_df.index)
            crime_types_info = [{'type': crime_type, 'values': list(all_months_df.loc[:, crime_type])} for crime_type in all_months_df.columns]

            results.append({'category': category, 'index_values': index_values, 'crime_types_info': crime_types_info})

    return results


def processDataForHorizontalBarChart(categories, year):
    results = []

    for category in categories:
        file_path = f"/home/kate/Desktop/TesisFinal/Categorias/{category}.csv"

        df = pd.read_csv(file_path)

        if 'Original_Date' in df.columns:
            df['Original_Date'] = pd.to_datetime(df['Original_Date'])

            df_filtered = df[df['Original_Date'].dt.year == int(year)]

            grouped_df = df_filtered.groupby('Primary_Type').size().sort_values(ascending=False)

            index_values = list(grouped_df.index)
            crime_types_info = [{'type': crime_type, 'values': [int(grouped_df[crime_type])]} for crime_type in grouped_df.index]
            results.append({'category': category, 'index_values': index_values, 'crime_types_info': crime_types_info})
    print("AQUI DATA PARA BARRAS HORIZONTALES----------",results)
    return results


def processDataForPolarChart(categories, year):

    community_file_path = "/home/kate/Desktop/TesisFinal/comunity_areas_names.csv"

    community_df = pd.read_csv(community_file_path)

    result_df = pd.DataFrame()

    for category in categories:

        crime_file_path = f"/home/kate/Desktop/TesisFinal/Categorias/{category}.csv"

        crime_df = pd.read_csv(crime_file_path)

        crime_df['Original_Date'] = pd.to_datetime(crime_df['Original_Date'])

        crime_df_filtered = crime_df[crime_df['Original_Date'].dt.year == int(year)]

        grouped_df = crime_df_filtered.groupby(['Community_Area', 'Primary_Type']).size().reset_index(name='Incidencias')

        result_df = pd.merge(community_df[['Community_Area', 'Community Area Name']], grouped_df, on='Community_Area', how='left').fillna(0)

    result_df['Incidencias'] = result_df['Incidencias'].astype(int)

    crime_types_info = []
    for crime_type in result_df['Primary_Type'].unique():
        values = list(result_df[result_df['Primary_Type'] == crime_type]['Incidencias'])
        # Asegurar que 'values' tenga la longitud correcta
        values += [0] * (len(community_df) - len(values))
        crime_types_info.append({'type': crime_type, 'values': values})

    result = [{
        'category': ', '.join(categories),
        'index_values': list(result_df['Community Area Name']),
        'crime_types_info': crime_types_info
    }]

    return result


def processDataForMap(categories, year, min_samples):
    result_data = {}

    for category in categories:

        crime_file_path = f"/home/kate/Desktop/TesisFinal/Categorias/{category}.csv"

        data = pd.read_csv(crime_file_path, parse_dates=['DateFull'])

        data_filtered = data[data['DateFull'].dt.year == int(year)]

        X = data_filtered[['Latitude', 'Longitude', 'DateFull', 'Primary_Type']].dropna()

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X[['Latitude', 'Longitude']])

        neigh = NearestNeighbors(n_neighbors=2)
        nbrs = neigh.fit(X_scaled)
        distances, indices = nbrs.kneighbors(X_scaled)

        # Calcular el gráfico de la distancia-k
        distances = np.sort(distances, axis=0)
        distances = distances[:, 1]

        kneedle = KneeLocator(range(len(distances)), distances, S=1.0, curve="convex", direction="increasing")

        optimal_eps = distances[kneedle.knee]
        print(f"Valor óptimo para eps: {optimal_eps}")

        dbscan = DBSCAN(eps=optimal_eps, min_samples=min_samples, metric='euclidean').fit(X_scaled)
        labels = dbscan.labels_

        X['ID_Cluster'] = labels
        result_data[category] = X[['Latitude', 'Longitude', 'DateFull', 'Primary_Type', 'ID_Cluster']].to_dict('records')

    return result_data
