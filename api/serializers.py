from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    rating = serializers.FloatField()
