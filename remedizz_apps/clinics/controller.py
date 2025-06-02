from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from remedizz_apps.clinics.views import *
from remedizz_apps.clinics.serializers import *
from remedizz_apps.common.swagger import SwaggerPage
from remedizz_apps.user.permissions import IsDigitalClinic


class ClinicController:

    @staticmethod
    @extend_schema(
        description="Retrieve all clinics.",
        responses=SwaggerPage.response(response=ClinicResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsDigitalClinic])
    def get_all_clinics(request: Request) -> Response:
        return ClinicView().get(request)

    @staticmethod
    @extend_schema(
        description="Retrieve a single clinic.",
        responses=SwaggerPage.response(response=ClinicResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsDigitalClinic])
    def get_clinic(request: Request, digital_clinic_id=None) -> Response:
        return ClinicView().get(request, digital_clinic_id=digital_clinic_id)



    @staticmethod
    @extend_schema(
        description="Delete clinic profile.",
        responses=SwaggerPage.response(description="clinic deleted successfully.")
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def delete_clinic(request: Request, digital_clinic_id: int) -> Response:
        return ClinicView().delete(request, digital_clinic_id)


    @staticmethod
    @extend_schema(
        description="Update clinic profile",
        request=ClinicRequestSerializer,
        responses=SwaggerPage.response(response=ClinicResponseSerializer)
    )
    @api_view(['PUT']) 
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def update_clinic(request: Request, digital_clinic_id: int) -> Response:
        return ClinicView().put(request, digital_clinic_id)
    


class ClinicMedicalRecordsController:

    @staticmethod
    @extend_schema(
        description="Retrieve medical records of a digital clinic.",
        responses=SwaggerPage.response(response=ClinicMedicalRecordResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def get_medical_record(request: Request, clinic_id: int) -> Response:
        return ClinicMedicalRecordsView().get(request, clinic_id)

    @staticmethod
    @extend_schema(
        description="Create medical records for a digital clinic.",
        request=ClinicMedicalRecordRequestSerializer,
        responses=SwaggerPage.response(response=ClinicMedicalRecordResponseSerializer)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def create_medical_record(request: Request) -> Response:
        return ClinicMedicalRecordsView().post(request)

    @staticmethod
    @extend_schema(
        description="Update medical records of a digital clinic.",
        request=ClinicMedicalRecordRequestSerializer,
        responses=SwaggerPage.response(response=ClinicMedicalRecordResponseSerializer)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def update_medical_record(request: Request, clinic_id: int) -> Response:
        return ClinicMedicalRecordsView().put(request, clinic_id)

    @staticmethod
    @extend_schema(
        description="Delete medical records of a digital clinic.",
        responses=SwaggerPage.response(description="Medical records deleted successfully.")
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def delete_medical_record(request: Request, clinic_id: int) -> Response:
        return ClinicMedicalRecordsView().delete(request, clinic_id)


class ClinicPaymentInfoController:

    @staticmethod
    @extend_schema(
        description="Retrieve payment info of a digital clinic.",
        responses=SwaggerPage.response(response=ClinicPaymentInfoResponseSerializer)
    )
    @api_view(['GET'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def get_payment_info(request: Request, digital_clinic_id: int) -> Response:
        return ClinicPaymentInfoView().get(request, digital_clinic_id)

    @staticmethod
    @extend_schema(
        description="Create payment info for a digital clinic.",
        request=ClinicPaymentInfoRequestSerializer,
        responses=SwaggerPage.response(response=ClinicPaymentInfoResponseSerializer)
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def create_payment_info(request: Request, digital_clinic_id: int) -> Response:
        return ClinicPaymentInfoView().post(request, digital_clinic_id)

    @staticmethod
    @extend_schema(
        description="Update payment info of a digital clinic.",
        request=ClinicPaymentInfoRequestSerializer,
        responses=SwaggerPage.response(response=ClinicPaymentInfoResponseSerializer)
    )
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def update_payment_info(request: Request, digital_clinic_id: int) -> Response:
        return ClinicPaymentInfoView().put(request, digital_clinic_id)

    @staticmethod
    @extend_schema(
        description="Delete payment info of a digital clinic.",
        responses=SwaggerPage.response(description="Payment info deleted successfully.")
    )
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated, IsDigitalClinic])
    def delete_payment_info(request: Request, digital_clinic_id: int) -> Response:
        return ClinicPaymentInfoView().delete(request, digital_clinic_id)