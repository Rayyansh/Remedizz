# Generated by Django 5.1.7 on 2025-05-22 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, max_length=50, null=True, upload_to='users/profile_pictures/'),
        ),
    ]
