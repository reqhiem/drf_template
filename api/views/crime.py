from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.Serializers.data import (
    DataSerializer,
    DataRobberySerializer,
    ProcessedDataChartSerializer,
    ProcessedDataLinesSerializer,
    ProcessedDataPolarSerializer
)
from api.utils import (
    get_by_type,
    get_type,
    get_geojson,
    get_clusters,
    get_comunity_areas,
    get_info_bar_polar,
    get_info_dot_map,
    processDataForBarChart,
    processDataForMultiLineChart,
    processDataForHorizontalBarChart,
    processDataForPolarChart,
    processDataForMap,
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@api_view(["GET"])
def alldata(request):
    primary_types = ['Homicidecomplete_', 'Assaultcomplete_', 'Narcoticscomplete_', 'Prostitutioncomplete_']

    data = get_by_type(primary_types)

    # Crea un diccionario para almacenar los resultados por fecha
    result = []

    current_date = None
    current_entry = None

    for index, row in data.iterrows():
        date = row['Date']
        if date != current_date:
            if current_entry is not None:
                result.append(current_entry)

            current_date = date
            current_entry = {
                'date': row['Datefull'],
                'total': row['TOTALES'],
                'details': []
            }

        detail_entry = {
            'name': row['Primary Type'],
            'value': row['Count'],
            'date': row['Datefull']
        }
        current_entry['details'].append(detail_entry)

    # Agrega el último entry
    if current_entry is not None:
        result.append(current_entry)

    serializer = DataSerializer(result, many=True)
    return Response(data=serializer.data)


@api_view(["GET"])
def battery(request):
    primary_types = ['Roobery']

    data = get_type(primary_types)
    serializer = DataRobberySerializer(data, many=True)
    return Response(data=serializer.data)


@api_view(["GET"])
def getmap(request):
    data = get_geojson()
    return Response(data=data)


@api_view(["GET"])
def getareas(request):
    data = get_comunity_areas()
    return Response(data=data)


@api_view(["GET"])
def getclusters(request):
    data = get_clusters()
    return Response(data=data)


@api_view(["GET"])
def getbarpolar(request):
    data = get_info_bar_polar()
    return Response(data=data)


@api_view(["GET"])
def getdotdata(request):
    data = get_info_dot_map()
    return Response(data=data)


@csrf_exempt
def get_crime(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos:", data)

            # Procesar los datos según tus necesidades
            categories = data.get('categories', [])
            year = data.get('year', '')
            min_samples = data.get('min_samples', 30)
            print("min_samples", min_samples)

            processed_data_horizontal = processDataForHorizontalBarChart(categories, year)
            processed_data_chart = processDataForBarChart(categories, year)
            processed_data_lines = processDataForMultiLineChart(categories, year)
            processed_data_polar = processDataForPolarChart(categories, year)
            processed_data_map = processDataForMap(categories, year, min_samples)
            print("PROCESSED DATA MAP", processed_data_map)

            serializer = ProcessedDataChartSerializer(data=processed_data_chart, many=True)
            serializer_lines = ProcessedDataLinesSerializer(data=processed_data_lines, many=True)
            serializer_horizontal = ProcessedDataLinesSerializer(data=processed_data_horizontal, many=True)
            serializer_polar = ProcessedDataPolarSerializer(data=processed_data_polar, many=True)
            # serializer_map = ClusterDataSerializer(data=processed_data_map, many=True)

            # print("MAP CLUSTERS SERIALIZER", serializer_map)

            # Verificar si los datos son válidos antes de acceder a .data
            if serializer.is_valid():
                serialized_chart_data = serializer.data
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data for processed_data_chart'})

            # Verificar si los datos son válidos antes de acceder a .data
            if serializer_lines.is_valid():
                serialized_chart_lines = serializer_lines.data
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data for processed_data_Lines'})

            if serializer_horizontal.is_valid():
                serialized_chart_horizontal = serializer_horizontal.data
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data for processed_data_horizontal_bar_chart'})

            if serializer_polar.is_valid():
                serialized_chart_polar = serializer_polar.data
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data for processed_data_Polar'})

            """ if serializer_map.is_valid():
                serialized_chart_map = serializer_map.data
            else:
                print(serializer.errors)
                return JsonResponse({'success': False, 'message': 'Invalid data for processed_data_Map'}) """

            # Devolver una respuesta exitosa con la data serializada
            return JsonResponse({
                'success': True,
                'processed_data_horizontal': serialized_chart_horizontal,
                'processed_data_chart': serialized_chart_data,
                'processed_data_lines': serialized_chart_lines,
                'processed_data_polar': serialized_chart_polar,
                'processed_data_map': processed_data_map,
            })
        except json.JSONDecodeError:
            # Devolver una respuesta de error si hay un problema con el formato JSON
            return JsonResponse({'success': False, 'message': 'Invalid JSON format in request body'})
    else:
        # Devolver una respuesta de error si no es una solicitud POST
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'})
