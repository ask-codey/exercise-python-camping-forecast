# Tests for forecast.py. Run them with: pytest (in the exercise folder, with the virtual environment active).
# Each test calls one of your functions with the values in its name and checks what it returns. A failing test
# says what it called, what it expected and what came back.
# The tests never use the network: they read the Weather Service's answers saved in saved/, and hand get_forecast
# stand-in fetch functions instead of the real one. You don't need to change this file.
import json
from datetime import date
from pathlib import Path

import requests

from forecast import POINTS_URL, forecast_url, get_forecast, packing_list, weekend_periods

SAVED = Path(__file__).parent.parent / "saved"
FORECAST_URL = "https://api.weather.gov/gridpoints/PQR/107,74/forecast"


def load(name):
    with open(SAVED / name, encoding="utf-8") as file:
        return json.load(file)


POINTS = load("points.json")
FORECAST = load("forecast.json")


def check(call, got, expected):
    """Fails with a message that says what the call returned and what it should return."""
    assert got == expected, f"{call} should return {expected!r}, but it returned {got!r}."


def period(name, temperature, rain_chance):
    """A period the way weekend_periods gives it, for the packing_list tests."""
    return {"name": name, "temperature": temperature, "rain_chance": rain_chance, "summary": "Test"}


def saved_answers(url):
    """A stand-in fetch: answers from the saved files, the way the Weather Service answered on 2026-11-17."""
    answers = {POINTS_URL: POINTS, FORECAST_URL: FORECAST}
    assert url in answers, f"get_forecast asked for {url}, which isn't the points address or the forecast address."
    return answers[url]


def no_connection(url):
    raise requests.exceptions.ConnectionError("no signal at the campground")


def too_slow(url):
    raise requests.exceptions.Timeout("no answer in 10 seconds")


def server_error(url):
    raise requests.exceptions.HTTPError("500 Server Error: Internal Server Error")


def copy_saved_on(tmp_path, saved_on):
    """Writes a saved copy of forecast.json, dated saved_on, in a temporary folder, and returns its path."""
    path = tmp_path / "forecast-copy.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump({"saved_on": saved_on, "forecast": FORECAST}, file)
    return path


def test_1_forecast_url_of_the_saved_points_answer_is_the_pqr_107_74_forecast():
    check("forecast_url(saved points.json)", forecast_url(POINTS), FORECAST_URL)


def test_2_forecast_url_of_a_points_answer_for_another_place_is_its_bou_62_61_forecast():
    other = {"properties": {"forecast": "https://api.weather.gov/gridpoints/BOU/62,61/forecast"}}
    check("forecast_url(an answer for BOU/62,61)", forecast_url(other),
          "https://api.weather.gov/gridpoints/BOU/62,61/forecast")


def test_3_weekend_periods_of_the_saved_forecast_are_saturday_to_sunday_night():
    names = [p["name"] for p in weekend_periods(FORECAST)]
    check("the names in weekend_periods(saved forecast.json)", names,
          ["Saturday", "Saturday Night", "Sunday", "Sunday Night"])


def test_4_weekend_periods_saturday_is_43_degrees_74_percent_light_rain_likely():
    check("weekend_periods(saved forecast.json)[0]", weekend_periods(FORECAST)[0],
          {"name": "Saturday", "temperature": 43, "rain_chance": 74, "summary": "Light Rain Likely"})


def test_5_weekend_periods_sunday_night_is_38_degrees_40_percent_chance_light_rain():
    check("weekend_periods(saved forecast.json)[3]", weekend_periods(FORECAST)[3],
          {"name": "Sunday Night", "temperature": 38, "rain_chance": 40, "summary": "Chance Light Rain"})


def test_6_weekend_periods_a_null_rain_chance_becomes_0():
    answer = {"properties": {"periods": [
        {"name": "Saturday", "temperature": 61, "probabilityOfPrecipitation": {"value": None},
         "shortForecast": "Sunny"},
    ]}}
    check("weekend_periods(a Saturday whose rain chance is None)", weekend_periods(answer),
          [{"name": "Saturday", "temperature": 61, "rain_chance": 0, "summary": "Sunny"}])


def test_7_weekend_periods_of_a_forecast_with_only_tonight_and_wednesday_is_empty():
    answer = {"properties": {"periods": [
        {"name": "Tonight", "temperature": 39, "probabilityOfPrecipitation": {"value": 72},
         "shortForecast": "Light Rain Likely"},
        {"name": "Wednesday", "temperature": 44, "probabilityOfPrecipitation": {"value": 31},
         "shortForecast": "Chance Light Rain"},
    ]}}
    check("weekend_periods(Tonight and Wednesday only)", weekend_periods(answer), [])


def test_8_packing_list_with_no_periods_is_tent_headlamp_water_bottles():
    check("packing_list([])", packing_list([]), ["tent", "headlamp", "water bottles"])


def test_9_packing_list_45_degrees_and_10_percent_rain_adds_nothing():
    check("packing_list([Saturday 45°F, 10% rain])", packing_list([period("Saturday", 45, 10)]),
          ["tent", "headlamp", "water bottles"])


def test_10_packing_list_exactly_50_percent_rain_adds_a_tarp():
    check("packing_list([Sunday 45°F, 50% rain])", packing_list([period("Sunday", 45, 50)]),
          ["tent", "headlamp", "water bottles", "tarp"])


def test_11_packing_list_49_percent_rain_adds_no_tarp():
    check("packing_list([Sunday 45°F, 49% rain])", packing_list([period("Sunday", 45, 49)]),
          ["tent", "headlamp", "water bottles"])


def test_12_packing_list_39_degrees_adds_a_warm_sleeping_bag():
    check("packing_list([Saturday Night 39°F, 10% rain])", packing_list([period("Saturday Night", 39, 10)]),
          ["tent", "headlamp", "water bottles", "warm sleeping bag"])


def test_13_packing_list_exactly_40_degrees_adds_no_warm_sleeping_bag():
    check("packing_list([Saturday Night 40°F, 10% rain])", packing_list([period("Saturday Night", 40, 10)]),
          ["tent", "headlamp", "water bottles"])


def test_14_packing_list_for_the_saved_weekend_adds_a_tarp_then_a_warm_sleeping_bag():
    check("packing_list(weekend_periods(saved forecast.json))", packing_list(weekend_periods(FORECAST)),
          ["tent", "headlamp", "water bottles", "tarp", "warm sleeping bag"])


def test_15_get_forecast_with_both_requests_working_returns_the_forecast_and_live(tmp_path):
    path = copy_saved_on(tmp_path, "2026-11-10")
    forecast, source = get_forecast(fetch=saved_answers, saved_path=path)
    check("get_forecast(a working fetch)'s source", source, "live")
    check("get_forecast(a working fetch)'s forecast == forecast.json", forecast == FORECAST, True)


def test_16_get_forecast_with_both_requests_working_saves_the_forecast_with_todays_date(tmp_path):
    path = copy_saved_on(tmp_path, "2026-11-10")
    get_forecast(fetch=saved_answers, saved_path=path)
    with open(path, encoding="utf-8") as file:
        saved = json.load(file)
    check("the saved copy's saved_on, after a live forecast,", saved.get("saved_on"), str(date.today()))
    check("the saved copy's forecast == forecast.json, after a live forecast,", saved.get("forecast") == FORECAST, True)


def test_17_get_forecast_with_no_connection_returns_the_saved_copy_from_2026_11_17(tmp_path):
    path = copy_saved_on(tmp_path, "2026-11-17")
    forecast, source = get_forecast(fetch=no_connection, saved_path=path)
    check("get_forecast(no connection)'s source", source, "saved copy from 2026-11-17")
    check("get_forecast(no connection)'s forecast == the saved copy's", forecast == FORECAST, True)


def test_18_get_forecast_with_a_timeout_returns_the_saved_copy_from_2026_11_17(tmp_path):
    path = copy_saved_on(tmp_path, "2026-11-17")
    forecast, source = get_forecast(fetch=too_slow, saved_path=path)
    check("get_forecast(a timeout)'s source", source, "saved copy from 2026-11-17")


def test_19_get_forecast_with_a_500_error_returns_the_saved_copy_from_2026_11_17(tmp_path):
    path = copy_saved_on(tmp_path, "2026-11-17")
    forecast, source = get_forecast(fetch=server_error, saved_path=path)
    check("get_forecast(a 500 error)'s source", source, "saved copy from 2026-11-17")
