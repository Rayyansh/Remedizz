from django.db import models

class City(models.Model):
    city_name = models.CharField(max_length=150)

    def __str__(self):
        return self.city_name

    @staticmethod
    def get_city_by_id(city_id):
        return City.objects.filter(id=city_id).first()

    @staticmethod
    def get_all_cities():
        return City.objects.all()

    @staticmethod
    def update_city(city_id, **kwargs):
        return City.objects.filter(id=city_id).update(**kwargs)

    @staticmethod
    def delete_city(city_id):
        return City.objects.filter(id=city_id).delete()
