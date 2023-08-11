from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import DataSerializer
from api.utils import get_by_type


@api_view(["GET"])
def alldata(request):
    primary_types = ['Homicidecomplete_', 'Assaultcomplete_']

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
                'Date': row['Datefull'],
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
