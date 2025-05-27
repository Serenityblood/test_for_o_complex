from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Никнейм"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Имейл"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Никнейм"}
            ),
            "password1": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Пароль"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Подтверждение пароля"}
            ),
        }
