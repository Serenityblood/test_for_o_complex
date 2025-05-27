import os
from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-z7wcbmlo1ebwmn9-fqxzb260o0f91$j&!09*-(*&7k_qc5-f*i"
)

IS_PRODUCTION = int(os.getenv("IS_PRODUCTION", 0))
DEBUG = False if IS_PRODUCTION else True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "user",
    "weather",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "user.middlewares.JWTAuthMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATE_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


if IS_PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MAX_NAME_DIGITS = int(os.getenv("MAX_NAME_DIGITS", 128))

AUTH_USER_MODEL = "user.User"

COOKIE_EXPIRE_TIME = int(os.getenv("COOKIE_EXPIRE_TIME", 86400))

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1"]

WEATHER_CODES = {
    0: "Чистое небо",
    1: "В основном ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Туман с отложением изморози",
    51: "Морось: слабая интенсивность",
    53: "Морось: умеренная интенсивность",
    55: "Морось: сильная интенсивность",
    56: "Замерзающая морось: слабая интенсивность",
    57: "Замерзающая морось: сильная интенсивность",
    61: "Дождь: слабая интенсивность",
    63: "Дождь: умеренная интенсивность",
    65: "Дождь: сильная интенсивность",
    66: "Замерзающий дождь: слабая интенсивность",
    67: "Замерзающий дождь: сильная интенсивность",
    71: "Снегопад: слабая интенсивность",
    73: "Снегопад: умеренная интенсивность",
    75: "Снегопад: сильная интенсивность",
    77: "Снежные зерна",
    80: "Ливень: слабая интенсивность",
    81: "Ливень: умеренная интенсивность",
    82: "Ливень: сильная интенсивность",
    85: "Снежный ливень: слабая интенсивность",
    86: "Снежный ливень: сильная интенсивность",
    95: "Гроза: слабая или умеренная",
    96: "Гроза с небольшим градом",
    99: "Гроза с сильным градом"
}