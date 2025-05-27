import datetime

import requests

from typing import Optional


def check_current_weather(latitude: float, longitude: float) -> Optional[dict]:
    """Возвращает температуру и состояние погоды на данный момент и в течение дня.
    Если в ходе запроса была ошибка - вернет None"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "current": ["temperature", "weather_code"], "hourly": ["temperature", "weather_code"], "forecast_days": 1}
    try:
        response = requests.get(url=url, params=params)
    # Ошибок во время запроса может быть много,
    # в тестовом проекте отлавливать все и выстраивать поведение функции от этого считаю излишним
    except Exception:
        return None
    if response.status_code != 200:
        return None
    return response.json()
