from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpRequest, HttpResponse

from .forms import LoginForm, RegisterForm


User = get_user_model()


def login(request: HttpRequest):
    """Вью для входа"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Используем authenticate для проверки пользователя
            user = authenticate(request, username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)

                response = redirect("weather:main")

                # Устанавливаем куки
                response.set_cookie(
                    key="jwt_token",
                    value=str(refresh.access_token),
                    httponly=True,
                    samesite="Lax",
                    max_age=settings.COOKIE_EXPIRE_TIME,
                )

                return response
            else:
                return render(request, "login.html", {"form": form, "no_user": True})
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def register(request: HttpRequest):
    """Вью для регистрации"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:login")  # Перенаправляем на страницу login
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def logout(request: HttpRequest):
    """Вью для выхода"""
    if request.user:
        response = redirect("weather:main")
        response.delete_cookie("jwt_token")
        return response
    return redirect("weather:main")
