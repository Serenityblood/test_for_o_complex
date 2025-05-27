import pytest
from unittest.mock import patch
from weather.utils import check_current_weather


@patch("weather.utils.requests.get")
def test_check_current_weather_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"current": {"temperature": 25}}

    result = check_current_weather(50.0, 30.0)
    assert result == {"current": {"temperature": 25}}


@patch("weather.utils.requests.get")
def test_check_current_weather_fail_status(mock_get):
    mock_get.return_value.status_code = 500

    result = check_current_weather(50.0, 30.0)
    assert result is None


@patch("weather.utils.requests.get", side_effect=Exception("Timeout"))
def test_check_current_weather_exception(mock_get):
    result = check_current_weather(50.0, 30.0)
    assert result is None
