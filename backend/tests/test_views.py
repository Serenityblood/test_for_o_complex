import pytest
from django.urls import reverse
from rest_framework import status
from weather.models import WeatherSearchHistory, City


@pytest.mark.django_db
def test_get_city_search_count(authenticated_client, city):
    WeatherSearchHistory.objects.create(
        city=city, user=authenticated_client.user, search_counter=5
    )
    WeatherSearchHistory.objects.create(
        city=city, user=authenticated_client.user, search_counter=3
    )

    url = reverse("api:city_stats", kwargs={"city_id": city.id})
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"city_id": city.id, "total_searches": 8}


@pytest.mark.django_db
def test_get_user_stats(authenticated_client, city):
    WeatherSearchHistory.objects.create(
        city=city, user=authenticated_client.user, search_counter=1
    )

    url = reverse("api:user_stats")
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["city"] == city.__str__()


@pytest.mark.django_db
def test_get_cities_list(authenticated_client):
    City.objects.create(
        name="City1", subject="Test1", district="Test1", latitude=1.00, longitude=2.00
    )
    City.objects.create(
        name="City2", subject="Test2", district="Test2", latitude=2.00, longitude=3.00
    )

    url = reverse("api:cities")
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_get_token_success(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="testpass"
    )

    url = reverse("api:get_token")
    response = client.post(url, data={"username": "testuser", "password": "testpass"})

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.json()


@pytest.mark.django_db
def test_get_token_failure(client):
    url = reverse("api:get_token")
    response = client.post(url, data={"username": "wrong", "password": "wrong"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.json()
