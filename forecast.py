"""Pine Ridge Campground's weekend forecast: four functions for you to finish.

The forecast comes from the US National Weather Service's API (api.weather.gov:
free, no key, open data). The docstring under each function says what it should
return, with examples. Replace each raise NotImplementedError("Not built yet.")
line with your own code. fetch_json at the top is ready to use.

The saved/ folder holds the Weather Service's real answers, saved on 2026-11-17:
points.json (the campground's point) and forecast.json (its forecast), plus
forecast-copy.json, the saved copy get_forecast falls back to.
"""
import json
from datetime import date

import requests

POINTS_URL = "https://api.weather.gov/points/44.8783,-122.6534"
HEADERS = {"User-Agent": "PythonCourseExample/1.0 (example@example.com)"}
WEEKEND = ["Saturday", "Saturday Night", "Sunday", "Sunday Night"]
SAVED_COPY = "saved/forecast-copy.json"


def fetch_json(url):
    """Ready to use: ask the Weather Service for url and return its JSON answer.

    Raises a requests.exceptions.RequestException (ConnectionError, Timeout or
    HTTPError) when the request fails.
    """
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def forecast_url(points_json):
    """Return the forecast's address from the Weather Service's points answer.

    It's the "forecast" value inside the answer's "properties".

    With saved/points.json:
    forecast_url(points) -> "https://api.weather.gov/gridpoints/PQR/107,74/forecast"
    """
    raise NotImplementedError("Not built yet.")


def weekend_periods(forecast_json):
    """Return the weekend's periods from a forecast answer, as small dictionaries.

    The answer's "properties" hold a list of "periods". Keep only the periods
    whose "name" is in WEEKEND ("Saturday", "Saturday Night", "Sunday" or
    "Sunday Night"), in the order they come. For each one, make a dictionary
    with four keys:

      "name": the period's "name"
      "temperature": its "temperature" (in degrees Fahrenheit)
      "rain_chance": the "value" inside its "probabilityOfPrecipitation",
                     or 0 when that value is None (the Weather Service sends
                     null when it has no number)
      "summary": its "shortForecast"

    With saved/forecast.json, the first of the four is:
    {"name": "Saturday", "temperature": 43, "rain_chance": 74, "summary": "Light Rain Likely"}

    A forecast with no weekend periods gives an empty list, [].
    """
    raise NotImplementedError("Not built yet.")


def packing_list(periods):
    """Return the packing list for a list of periods like weekend_periods gives.

    Every trip packs "tent", "headlamp" and "water bottles", in that order.
    Then:
      - add "tarp" when any period's rain_chance is 50 or more;
      - add "warm sleeping bag" when any period's temperature is below 40.
    The tarp comes before the warm sleeping bag when both are added.

    packing_list([]) -> ["tent", "headlamp", "water bottles"]
    packing_list([{"name": "Saturday", "temperature": 43, "rain_chance": 74, "summary": "Light Rain Likely"},
                  {"name": "Saturday Night", "temperature": 38, "rain_chance": 74, "summary": "Light Rain Likely"}])
        -> ["tent", "headlamp", "water bottles", "tarp", "warm sleeping bag"]
    """
    raise NotImplementedError("Not built yet.")


def get_forecast(fetch=fetch_json, saved_path=SAVED_COPY):
    """Return the forecast answer and where it came from, as two values.

    fetch is the function that asks the Weather Service: it takes a URL and
    returns the JSON answer, or raises a requests.exceptions.RequestException.
    The real one is fetch_json; tests hand in stand-ins.

    1. Call fetch(POINTS_URL) for the point's answer, find the forecast's
       address in it with forecast_url, and call fetch with that address for
       the forecast.
    2. When both requests work: save {"saved_on": <today>, "forecast": <the forecast>}
       to saved_path as JSON, where <today> is str(date.today()), such as
       "2026-11-21". Then return the forecast and "live".
    3. When fetch raises a requests.exceptions.RequestException: load the
       saved copy from saved_path and return its "forecast" and
       "saved copy from " followed by its "saved_on", such as
       "saved copy from 2026-11-17".

    You don't need to handle a missing saved copy: the exercise ships one.
    """
    raise NotImplementedError("Not built yet.")
