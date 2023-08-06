from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    case_number = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.get('ID')

    def get_case_number(self, obj):
        return obj.get('Case Number')

    def get_date(self, obj):
        return obj.get('Date')
