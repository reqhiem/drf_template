from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import DataSerializer
from api.utils import get_by_years


@api_view(["GET"])
def alldata(request):
    data = get_by_years(year_start=1990, year_end=2000)
    serializer = DataSerializer(data, many=True)
    return Response(data=serializer.data)
