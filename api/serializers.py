from rest_framework import serializers

"""
an object is like:
{
    "ID": 12571973,
    "Case Number": "JE482457",
    "Date": "12/19/2021 07:23:00 AM",
    "Block": "042XX S MOZART ST",
    "IUCR": "0460",
    "Primary Type": "BATTERY",
    "Description": "SIMPLE",
    "Location Description": "SIDEWALK",
    "Arrest": true,
    "Domestic": true,
    "Beat": 921,
    "District": 9.0,
    "Ward": 15.0,
    "Community Area": 58.0,
    "FBI Code": "08B",
    "X Coordinate": 1158067.0,
    "Y Coordinate": 1876425.0,
    "Year": 2021,
    "Updated On": "09/12/2022 04:45:45 PM",
    "Latitude": 41.81665685,
    "Longitude": -87.695688608,
    "Location": "(41.81665685, -87.695688608)"
}
"""


class DataSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    case_number = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    block = serializers.SerializerMethodField()
    iucr = serializers.SerializerMethodField()
    primary_type = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    location_description = serializers.SerializerMethodField()
    arrest = serializers.SerializerMethodField()
    domestic = serializers.SerializerMethodField()
    beat = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    """ ward = serializers.SerializerMethodField()
    community_area = serializers.SerializerMethodField()
    fbi_code = serializers.SerializerMethodField()
    x_coordinate = serializers.SerializerMethodField()
    y_coordinate = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    updated_on = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField() """

    def get_id(self, obj):
        return obj.get('ID')

    def get_case_number(self, obj):
        return obj.get('Case Number')

    def get_date(self, obj):
        return obj.get('Date')

    def get_block(self, obj):
        return obj.get('Block')

    def get_iucr(self, obj):
        return obj.get('IUCR')

    def get_primary_type(self, obj):
        return obj.get('Primary Type')

    def get_description(self, obj):
        return obj.get('Description')

    def get_location_description(self, obj):
        return obj.get('Location Description')

    def get_arrest(self, obj):
        return obj.get('Arrest')

    def get_domestic(self, obj):
        return obj.get('Domestic')

    def get_beat(self, obj):
        return obj.get('Beat')

    def get_district(self, obj):
        return obj.get('District')
