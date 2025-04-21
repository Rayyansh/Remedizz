from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from remedizz_apps.gender.views import GenderView
from remedizz_apps.gender.serializers import GenderRequestSerializer, GenderResponseSerializer
from remedizz_apps.common.swagger import SwaggerPage
from django.http import HttpRequest

class GenderController:

    @staticmethod
    @extend_schema(
        description="Retrieve all genders.",
        responses=SwaggerPage.response(response=GenderResponseSerializer)
    )
    @api_view(['GET'])
    def get_all_genders(request):
        return GenderView.as_view()(request._request)

    @staticmethod
    @extend_schema(
        description="Retrieve a single gender.",
        responses=SwaggerPage.response(response=GenderResponseSerializer)
    )
    @api_view(['GET'])
    def get_gender_by_id(request, gender_id):
        return GenderView.as_view()(request._request, gender_id=gender_id)
    
    @staticmethod
    @extend_schema(
        description="Create a new gender.",
        request= GenderRequestSerializer,
        responses=SwaggerPage.response(response= GenderResponseSerializer)
    )
    @api_view(['POST'])
    def create_gender(request):
        return GenderView.as_view()(request._request)

    @staticmethod
    @extend_schema(
        description="Update gender information.",
        request= GenderRequestSerializer,
        responses=SwaggerPage.response(response= GenderResponseSerializer)
    )
    @api_view(['PUT'])
    def update_gender(request, gender_id):
        return GenderView.as_view()(request._request, gender_id=gender_id)

    @staticmethod
    @extend_schema(
        description="Delete a gender.",
        responses=SwaggerPage.response(description="Gender deleted successfully.")
    )
    @api_view(['DELETE'])
    def delete_gender(request, gender_id):
        return GenderView.as_view()(request._request, gender_id=gender_id)
