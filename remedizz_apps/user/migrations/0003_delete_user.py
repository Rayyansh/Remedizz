# Generated by Django 5.1.7 on 2025-03-27 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
