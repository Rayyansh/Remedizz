from rest_framework import serializers
from remedizz_apps.gender.models import Gender



class GenderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['gender_name']

class GenderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'gender_name']
