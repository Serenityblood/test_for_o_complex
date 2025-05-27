from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Sum
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    OpenApiExample,
)

from .serializers import LoginSerializer, CitySerializer, WeatherSearchHistorySerializer
from weather.models import City, WeatherSearchHistory


User = get_user_model()


@extend_schema(
    methods=["POST"],
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="JWT access-токен",
            examples=[
                OpenApiExample(
                    name="Успешный вход",
                    value={"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJI..."},
                    status_codes=["200"],
                )
            ],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Неверные учётные данные",
            examples=[
                OpenApiExample(
                    name="Ошибка аутентификации",
                    value={
                        "error": "Юзера с такими юзернеймном и паролем не существует"
                    },
                    status_codes=["400"],
                )
            ],
        ),
    },
    summary="Получить JWT токен",
    description="Аутентификация пользователя и возврат JWT access-токена.",
)
@api_view(["POST"])
def get_token(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        request=request,
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )
    if user:
        token = RefreshToken.for_user(user)
        return Response({"access": f"{token.access_token}"}, status=status.HTTP_200_OK)
    return Response(
        {"error": "Юзера с такими юзернеймном и паролем не существует"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@extend_schema(
    methods=["GET"],
    responses=CitySerializer(many=True),
    summary="Получить список городов",
    description="Возвращает список всех доступных городов. Требуется аутентификация.",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cities_list(request: Request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=["GET"],
    responses=WeatherSearchHistorySerializer(many=True),
    summary="Получить историю запросов пользователя",
    description="Возвращает историю запросов погоды для текущего пользователя. Требуется аутентификация.",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_stats(request: Request):
    user = request.user
    searches = WeatherSearchHistory.objects.filter(user=user)
    serializer = WeatherSearchHistorySerializer(searches, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=["GET"],
    parameters=[
        OpenApiParameter(
            name="city_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            required=True,
            description="ID города",
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Сумма всех запросов по городу",
            examples=[
                OpenApiExample(
                    name="Пример успешного ответа",
                    value={"city_id": 1, "total_searches": 42},
                    status_codes=["200"],
                )
            ],
        )
    },
    summary="Получить общее количество поисков по городу",
    description="Возвращает сумму всех `search_counter` для заданного города. Требуется аутентификация.",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_city_search_count(request: Request, city_id: int):
    total = WeatherSearchHistory.objects.filter(city_id=city_id).aggregate(
        total_searches=Sum("search_counter")
    )
    return Response(
        {
            "city_id": city_id,
            "total_searches": total["total_searches"] if total["total_searches"] else 0,
        },
        status=status.HTTP_200_OK,
    )
