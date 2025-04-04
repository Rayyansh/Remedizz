from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from remedizz_apps.user.permissions import IsPatient

from remedizz_apps.patients.views import PatientView
from remedizz_apps.patients.serializers import PatientRequestSerializer, PatientResponseSerializer
from remedizz_apps.common.swagger import SwaggerPage


class PatientController:

    @extend_schema(
        description="Retrieve a single patient or all patients",
        responses=SwaggerPage.response(response=PatientResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsPatient])
    def get_patient(request: Request, patient_id=None) -> Response:
        return PatientView().get(request, patient_id)

    @extend_schema(
        description="Update patient profile",
        request=PatientRequestSerializer,
        responses=SwaggerPage.response(response=PatientResponseSerializer)
    )
    @api_view(['PUT'])
    def update_patient(request: Request, patient_id) -> Response:
        return PatientView().put(request, patient_id=patient_id)

    @extend_schema(
        description="Delete patient profile",
        responses=SwaggerPage.response(description="Patient deleted successfully.")
    )
    @api_view(['DELETE'])
    def delete_patient(request: Request, patient_id) -> Response:
        return PatientView().delete(request, patient_id=patient_id)
