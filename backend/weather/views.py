import datetime
from django.shortcuts import render
from django.http import HttpRequest

from .forms import CityForm
from .models import WeatherSearchHistory
from .utils import check_current_weather


def main(request: HttpRequest):
    """View для основной страницы с запросами по погоде"""
    # Запрос на информацию по погоде
    if request.method == "POST":
        form = CityForm(request.POST)
        # Проверяем форму
        if form.is_valid():
            city = form.cleaned_data["city"]

            # Получаем данные о погоде
            weather_info = check_current_weather(
                latitude=city.latitude, longitude=city.longitude
            )
            # Если при получении погоды возникла ошибка - отразим это в шаблоне
            if not weather_info:
                return render(
                    request,
                    "main.html",
                    {"city": city, "weather_error": True, "form": form},
                )

            # Если юзер залогинился сохраняем данные о поисковом запросе
            if not request.user.is_anonymous:
                history, created = WeatherSearchHistory.objects.get_or_create(
                    user=request.user,
                    city=city,
                )

                # Если запрос уже был инкрементируем счетчик
                if not created:
                    history.search_counter += 1
                    history.save()
            # Передаем данные о погоде и городе в шаблон
            new_hourly = []
            hourly = weather_info['hourly']
            i = 0
            while i < len(hourly['time']) and i < len(hourly['temperature']):
                new_hourly.append({"time": datetime.datetime.fromisoformat(hourly["time"][i]), "temperature": hourly["temperature"][i]})
                i += 1
            weather_info["hourly"] = new_hourly
            return render(
                request,
                "main.html",
                {"city": city, "weather": weather_info, "form": form},
            )
    else:
        form = CityForm()

        if not request.user.is_anonymous:
            # Проверяем, есть ли у пользователя история поиска
            last_search = (
                WeatherSearchHistory.objects.filter(user=request.user)
                .order_by("-id")
                .first()
            )
            if last_search:
                # Предлагаем посмотреть погоду в последнем городе поиска
                return render(
                    request, "main.html", {"form": form, "last_city": last_search.city}
                )

    return render(request, "main.html", {"form": form})
