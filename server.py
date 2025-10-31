import openmeteo_requests

from datetime import datetime
from fastmcp import FastMCP
from typing import List, TypedDict
from zoneinfo import ZoneInfo

LATITUDE = -30.0328
LONGITUDE = -51.2302
TIMEZONE_NAME = "America/Sao_Paulo"
FORECAST_DAYS = 16

WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partially cloudy",
    3: "overcast",
    45: "fog",
    48: "rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow fall",
    73: "moderate snow fall",
    75: "heavy snow fall",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "heavy rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "slight or moderate thunderstorms",
    96: "thunderstorms with slight hail",
    99: "thunderstorms with heavy hail",
}


class CurrentWeather(TypedDict):
    timestamp: str           # ISO-8601 string
    temperature: float
    rain: float
    weather_code: int

class DailyForecast(TypedDict):
    timestamp: str           # ISO-8601 string
    min_temperature: float
    max_temperature: float
    rain_probability: int
    weather_code: int

class WeatherPayload(TypedDict):
    current_weather: CurrentWeather
    forecasts: List[DailyForecast]


mcp = FastMCP("mvfm's mcp server")


@mcp.tool
def add(a: int, b: int) -> int:
    """
    Adds two numbers.
    """
    return a + b


@mcp.tool
def now() -> datetime:
    """
    Returns the current date and time in America/Sao_Paulo's timezone.
    """
    return datetime.now(ZoneInfo(TIMEZONE_NAME))


@mcp.tool
def weather() -> WeatherPayload:
    """
    Returns the Porto Alegre's current weather conditions (temperature, rain amount, weather code and description), and
    the forecast for the next 16 days (the minimum and maximum temperatures, chance of rain, weather code and
    description).
    """
    openmeteo = openmeteo_requests.Client()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": ["temperature_2m_min", "temperature_2m_max", "precipitation_probability_max", "weather_code"],
        "current": ["temperature_2m", "rain", "weather_code"],
        "timezone": TIMEZONE_NAME,
        "forecast_days": FORECAST_DAYS,
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Get the current conditions.
    current = response.Current()
    current_weather: CurrentWeather = {
        "timestamp":    datetime.fromtimestamp(current.Time(), ZoneInfo(TIMEZONE_NAME)).isoformat(),
        "temperature":  current.Variables(0).Value(),
        "rain":         current.Variables(1).Value(),
        "weather_code": int(current.Variables(2).Value())
    }

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()

    # Build the list of timestamps (TimeEnd() is exclusive)
    start = daily.Time()     # UNIX seconds of first day
    end = daily.TimeEnd()    # UNIX seconds AFTER the last day
    step = daily.Interval()  # seconds between entries (daily ≈ 86400)

    timestamps = list(range(start, end, step))
    dates = [datetime.fromtimestamp(t, ZoneInfo(TIMEZONE_NAME)) for t in timestamps]

    forecasts: List[DailyForecast] = []

    # Loop using Values(i) for each variable
    for i, d in enumerate(dates):
        forecast: DailyForecast = {
            "timestamp": d.isoformat(),
            "min_temperature": daily.Variables(0).Values(i),
            "max_temperature": daily.Variables(1).Values(i),
            "rain_probability": int(daily.Variables(2).Values(i)),
            "weather_code": int(daily.Variables(3).Values(i)),
        }

        forecasts.append(
            forecast
        )

    result: WeatherPayload = {
        "current_weather": current_weather,
        "forecasts": forecasts,
    }

    return result



if __name__ == "__main__":
    mcp.run()
