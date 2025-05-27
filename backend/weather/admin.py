from django.contrib import admin

from .models import City, WeatherSearchHistory


admin.site.register(City)
admin.site.register(WeatherSearchHistory)
