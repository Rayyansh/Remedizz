from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from remedizz_apps.city.models import City
from remedizz_apps.common.common import Common
from remedizz_apps.city.serializers import CityRequestSerializer, CityResponseSerializer

class CityView(APIView):

    @Common().exception_handler
    def post(self, request):
        serializer = CityRequestSerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.save()
            return Response(CityResponseSerializer(city).data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @Common().exception_handler
    def get(self, request, city_id=None):
        if city_id:
            city = City.get_city_by_id(city_id)
            if city:
                serializer = CityResponseSerializer(city)
                return Response(serializer.data)
            return Response({"detail": "City not found."}, status=status.HTTP_404_NOT_FOUND)
        cities = City.get_all_cities()
        serializer = CityResponseSerializer(cities, many=True)
        return Response(serializer.data)

    @Common().exception_handler
    def put(self, request, city_id):
        city = City.get_city_by_id(city_id)
        if not city:
            return Response({"detail": "City not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CityRequestSerializer(city, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @Common().exception_handler
    def delete(self, request, city_id):
        city = City.get_city_by_id(city_id)
        if not city:
            return Response({"detail": "City not found."}, status=status.HTTP_404_NOT_FOUND)

        city.delete()
        return Response({"detail": "City deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
