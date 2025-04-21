from django.db import models

class Gender(models.Model):
    gender_name = models.CharField(max_length=150)

    def __str__(self):
        return self.gender_name

    @staticmethod
    def get_gender_by_id(gender_id):
        return Gender.objects.filter(id=gender_id).first()

    @staticmethod
    def get_all_genders():
        return Gender.objects.all()

    @staticmethod
    def update_gender(gender_id, **kwargs):
        return Gender.objects.filter(id=gender_id).update(**kwargs)

    @staticmethod
    def delete_gender(gender_id):
        return Gender.objects.filter(id=gender_id).delete()
