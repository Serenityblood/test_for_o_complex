from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


class City(models.Model):
    name = models.CharField(
        max_length=settings.MAX_NAME_DIGITS, blank=False, null=False
    )
    subject = models.CharField(
        max_length=settings.MAX_NAME_DIGITS, blank=False, null=False
    )
    district = models.CharField(
        max_length=settings.MAX_NAME_DIGITS, blank=False, null=False
    )
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.name}, {self.subject}, {self.district}"


class WeatherSearchHistory(models.Model):
    user = models.ForeignKey(
        User, related_name="search_history", on_delete=models.CASCADE
    )
    city = models.ForeignKey(City, related_name="searched_by", on_delete=models.CASCADE)
    search_counter = models.PositiveIntegerField(default=1, blank=False, null=False)
