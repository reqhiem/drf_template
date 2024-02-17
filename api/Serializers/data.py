from rest_framework import serializers
from datetime import datetime


class DataDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    date = serializers.DateTimeField(format='%a %b %d %Y %H:%M:%S GMT-0500 (Peru Standard Time)')
    value = serializers.IntegerField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'name': representation['name'],
            'date': representation['date'],  # Mantén la fecha como objeto DateTime
            'value': representation['value']
        }


class DataSerializer(serializers.Serializer):
    date = serializers.DateTimeField(format='%a %b %d %Y %H:%M:%S GMT-0500 (Peru Standard Time)')
    total = serializers.IntegerField()
    details = DataDetailSerializer(many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class DataRobberySerializer(serializers.Serializer):
    Primary_Type = serializers.CharField()
    District = serializers.CharField()
    Community_Area = serializers.IntegerField()
    Latitude = serializers.FloatField()
    Longitude = serializers.FloatField()
    Datefull = serializers.DateTimeField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class CrimeTypeSerializer(serializers.Serializer):
    type = serializers.CharField()
    values = serializers.ListField(child=serializers.IntegerField())


class ProcessedDataChartSerializer(serializers.Serializer):
    category = serializers.CharField()
    index_values = serializers.ListField(child=serializers.IntegerField())
    crime_types_info = CrimeTypeSerializer(many=True)


class ProcessedDataLinesSerializer(serializers.Serializer):
    category = serializers.CharField()
    index_values = serializers.ListField(child=serializers.CharField())
    crime_types_info = CrimeTypeSerializer(many=True)


class ProcessedDataHorizontalSerializer(serializers.Serializer):
    category = serializers.CharField()
    index_values = serializers.ListField(child=serializers.CharField())
    crime_types_info = CrimeTypeSerializer(many=True)


class ProcessedDataPolarSerializer(serializers.Serializer):
    category = serializers.CharField()
    index_values = serializers.ListField(child=serializers.CharField())
    crime_types_info = CrimeTypeSerializer(many=True)

