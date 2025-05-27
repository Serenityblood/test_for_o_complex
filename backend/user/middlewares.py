from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_token = request.COOKIES.get("jwt_token")
        if jwt_token:
            try:
                # Проверяем валидность токена
                access_token = AccessToken(jwt_token)
                access_token.verify()
                # Используем get т.к. либо мы получаем id, либо ошибку токена
                request.user = User.objects.get(id=access_token.payload["user_id"])
            except Exception as ex:
                return HttpResponse(
                    "В куки файле была ошибка, либо время жизни закончилось. Нужно войти снова",
                    status=403,
                ).delete_cookie("jwt_token")
