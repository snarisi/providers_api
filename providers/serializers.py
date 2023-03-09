from rest_framework import serializers


class ProviderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    sex = serializers.CharField()
    birth_date = serializers.DateField()
    rating = serializers.FloatField()
    primary_skills = serializers.ListField()
    secondary_skills = serializers.ListField()
    company = serializers.CharField()
    active = serializers.BooleanField()
    country = serializers.CharField()
    language = serializers.CharField()
    search_returns = serializers.IntegerField()
