from django.urls import path, include

from .views import login, logout, register

app_name = "user"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]
