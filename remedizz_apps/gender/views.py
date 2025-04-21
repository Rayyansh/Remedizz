from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from remedizz_apps.gender.models import Gender
from remedizz_apps.common.common import Common
from remedizz_apps.gender.serializers import *

class GenderView(APIView):

    @Common().exception_handler
    def post(self, request):
        serializer = GenderRequestSerializer(data=request.data)
        if serializer.is_valid():
            gender = serializer.save()
            return Response(GenderResponseSerializer(gender).data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @Common().exception_handler
    def get(self, request, gender_id=None):
        if gender_id:
            gender = Gender.get_gender_by_id(gender_id)
            if gender:
                serializer = GenderResponseSerializer(gender)
                return Response(serializer.data)
            return Response({"detail": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)
        genders = Gender.get_all_genders()
        serializer = GenderResponseSerializer(genders, many=True)
        return Response(serializer.data)

    @Common().exception_handler
    def put(self, request, gender_id):
        gender = Gender.get_gender_by_id(gender_id)
        if not gender:
            return Response({"detail": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GenderRequestSerializer(gender, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, gender_id):
        gender = Gender.get_gender_by_id(gender_id)
        if not gender:
            return Response({"detail": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

        gender.delete()
        return Response({"detail": "Gender deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
