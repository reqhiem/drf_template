from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import DataSerializer
from api.utils import get_by_year


@api_view(["GET"])
def alldata(request):
    data = get_by_year(year=2021)
    serializer = DataSerializer(data, many=True)
    return Response(data=serializer.data)
