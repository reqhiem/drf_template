from rest_framework import serializers


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
    Date = serializers.DateTimeField(format='%a %b %d %Y %H:%M:%S GMT-0500 (Peru Standard Time)')
    total = serializers.IntegerField()
    details = DataDetailSerializer(many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
