from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from remedizz_apps.user.permissions import IsPatient

from remedizz_apps.patients.views import PatientView, ChildPatientView
from remedizz_apps.patients.serializers.request.patient_create import PatientRequestSerializer
from remedizz_apps.patients.serializers.response.patient_get_all import PatientResponseSerializer
from remedizz_apps.patients.serializers.request.child_patient_create import ChildPatientRequestSerializer
from remedizz_apps.patients.serializers.response.child_patient_get_all import ChildPatientResponseSerializer
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

class ChildPatientController:

    @extend_schema(
        description="Create child patient profile",
        request=ChildPatientRequestSerializer,
        responses=SwaggerPage.response(description="Child created")
    )
    @api_view(['POST'])
    @permission_classes([IsPatient])
    def create_child(request):
        return ChildPatientView().post(request)

    @extend_schema(
        description="Get all or one child profile",
        responses=SwaggerPage.response(response=ChildPatientResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsPatient])
    def get_children(request, child_id=None):
        return ChildPatientView().get(request, child_id)

    @extend_schema(
        description="Update a child profile",
        request=ChildPatientRequestSerializer,
        responses=SwaggerPage.response(response=ChildPatientResponseSerializer)
    )
    @api_view(['PUT'])
    @permission_classes([IsPatient])
    def update_child(request, child_id):
        return ChildPatientView().put(request, child_id)

    @extend_schema(
        description="Delete a child profile",
        responses=SwaggerPage.response(description="Child deleted")
    )
    @api_view(['DELETE'])
    @permission_classes([IsPatient])
    def delete_child(request, child_id):
        return ChildPatientView().delete(request, child_id)
