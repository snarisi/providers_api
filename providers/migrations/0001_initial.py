# Generated by Django 4.1.7 on 2023-03-08 22:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Providers',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=500)),
                ('last_name', models.CharField(max_length=500)),
                ('sex', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('rating', models.FloatField()),
                ('primary_skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=100)),
                ('secondary_skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=100)),
                ('company', models.CharField(max_length=100)),
                ('active', models.BooleanField()),
                ('country', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
            ],
        ),
    ]
