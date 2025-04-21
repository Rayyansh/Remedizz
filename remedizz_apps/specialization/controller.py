from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from remedizz_apps.specialization.views import SpecializationView
from remedizz_apps.specialization.serializers import *
from remedizz_apps.common.swagger import SwaggerPage
from django.http import HttpRequest

class SpecializationrController:

    @staticmethod
    @extend_schema(
        description="Retrieve all specialization.",
        responses=SwaggerPage.response(response=SpecializationResponseSerializer)
    )
    @api_view(['GET'])
    def get_all_specialization(request):
        return SpecializationView.as_view()(request._request)

    @staticmethod
    @extend_schema(
        description="Retrieve a single specialization.",
        responses=SwaggerPage.response(response=SpecializationResponseSerializer)
    )
    @api_view(['GET'])
    def get_specialization_by_id(request, specialization_id):
        return SpecializationView.as_view()(request._request, specialization_id=specialization_id)
    
    @staticmethod
    @extend_schema(
        description="Create a new specialization.",
        request= SpecializationRequestSerializer,
        responses=SwaggerPage.response(response= SpecializationResponseSerializer)
    )
    @api_view(['POST'])
    def create_specialization(request):
        return SpecializationView.as_view()(request._request)

    @staticmethod
    @extend_schema(
        description="Update specialization information.",
        request= SpecializationRequestSerializer,
        responses=SwaggerPage.response(response= SpecializationResponseSerializer)
    )
    @api_view(['PUT'])
    def update_specialization(request, specialization_id):
        return SpecializationView.as_view()(request._request, specialization_id=specialization_id)

    @staticmethod
    @extend_schema(
        description="Delete a specialization.",
        responses=SwaggerPage.response(description="Specialization deleted successfully.")
    )
    @api_view(['DELETE'])
    def delete_specialization(request, specialization_id):
        return SpecializationView.as_view()(request._request, specialization_id=specialization_id)
