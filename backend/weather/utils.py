import datetime

import requests

from typing import Optional


def check_current_weather(latitude: float, longitude: float) -> Optional[dict]:
    """Возвращает температуру на данный момент по указанным координатам.
    Если в ходе запроса была ошибка - вернет None"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "current": ["temperature"], "hourly": ["temperature"], "forecast_days": 1}
    try:
        response = requests.get(url=url, params=params)
    # Ошибок во время запроса может быть много,
    # в тестовом проекте отлавливать все и выстраивать поведение функции от этого считаю излишним
    except Exception:
        return None
    if response.status_code != 200:
        return None
    return response.json()


if __name__ == "__main__":
    print(check_current_weather(52.65, 90.08333))
