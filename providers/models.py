from django.db import models
from django.contrib.postgres.fields import ArrayField


class Providers(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    sex = models.CharField(max_length=100)
    birth_date = models.DateField()
    rating = models.FloatField()
    primary_skills = ArrayField(models.CharField(max_length=100), size=100)
    secondary_skills = ArrayField(models.CharField(max_length=100), size=100)
    company = models.CharField(max_length=100)
    active = models.BooleanField()
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=100)

    # the number of times a provider has been returned by a search
    search_returns = models.IntegerField(default=0, editable=False)
