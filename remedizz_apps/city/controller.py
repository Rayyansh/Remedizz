from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from remedizz_apps.city.views import CityView
from remedizz_apps.city.serializers import CityRequestSerializer, CityResponseSerializer
from remedizz_apps.common.swagger import SwaggerPage
from django.http import HttpRequest

class CityController:

    @staticmethod
    @extend_schema(
        description="Retrieve all cities.",
        responses=SwaggerPage.response(response=CityResponseSerializer)
    )
    @api_view(['GET'])
    def get_all_cities(request):
        return CityView.as_view()(request._request)

    @staticmethod
    @extend_schema(
        description="Retrieve a single city.",
        responses=SwaggerPage.response(response=CityResponseSerializer)
    )
    @api_view(['GET'])
    def get_city_by_id(request, city_id):
        return CityView.as_view()(request._request, city_id=city_id)
    
    @staticmethod
    @extend_schema(
        description="Create a new city.",
        request=CityRequestSerializer,
        responses=SwaggerPage.response(response=CityResponseSerializer)
    )
    @api_view(['POST'])
    def create_city(request):
        return CityView.as_view()(request._request)

    @staticmethod
    @extend_schema(
        description="Update city information.",
        request=CityRequestSerializer,
        responses=SwaggerPage.response(response=CityResponseSerializer)
    )
    @api_view(['PUT'])
    def update_city(request, city_id):
        return CityView.as_view()(request._request, city_id=city_id)

    @staticmethod
    @extend_schema(
        description="Delete a city.",
        responses=SwaggerPage.response(description="City deleted successfully.")
    )
    @api_view(['DELETE'])
    def delete_city(request, city_id):
        return CityView.as_view()(request._request, city_id=city_id)
