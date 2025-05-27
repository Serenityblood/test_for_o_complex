import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from weather.models import City


User = get_user_model()


@pytest.fixture
def user(db):
    user = User.objects.create_user(username="test", email="test@test.test")
    user.set_password("pass")
    user.save()
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    client.user = user
    return client


@pytest.fixture
def city():
    return City.objects.create(
        name="Moscow", subject="Test", district="Test", latitude=50.01, longitude=30.01
    )
