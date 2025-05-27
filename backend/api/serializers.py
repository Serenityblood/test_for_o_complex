from django.conf import settings
from rest_framework import serializers

from weather.models import City, WeatherSearchHistory


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.MAX_NAME_DIGITS, required=True)
    password = serializers.CharField(required=True)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class WeatherSearchHistorySerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = WeatherSearchHistory
        fields = ["city", "search_counter"]
