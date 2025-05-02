from django.urls import path
from remedizz_apps.city.controller import CityController

urlpatterns = [
    path('create/', CityController.create_city, name='create_city'),  # create
    path('', CityController.get_all_cities, name='city-list-create'),  # get all
    path('<int:city_id>/', CityController.get_city_by_id, name='city-retrieve'),  # get specific
    path('update/<int:city_id>/', CityController.update_city, name='update_city'),  # update
    path('delete/<int:city_id>/', CityController.delete_city, name='delete_city'),  # delete
]
