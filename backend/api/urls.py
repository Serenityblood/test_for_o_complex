from django.urls import path, include

from .views import get_token, get_user_stats, get_cities_list, get_city_search_count

app_name = "api"

urlpatterns = [
    path("get_token/", get_token, name="get_token"),
    path("get_user_stats/", get_user_stats, name="user_stats"),
    path("cities/", get_cities_list, name="cities"),
    path("cities/<int:city_id>/", get_city_search_count, name="city_stats"),
]
