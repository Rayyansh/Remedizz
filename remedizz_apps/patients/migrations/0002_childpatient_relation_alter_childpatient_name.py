# Generated by Django 5.1.7 on 2025-04-22 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='childpatient',
            name='relation',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='childpatient',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
