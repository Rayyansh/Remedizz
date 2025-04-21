from rest_framework import serializers
from remedizz_apps.city.models import City



class CityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']

class CityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name']
