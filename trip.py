# Prints Pine Ridge Campground's weekend forecast and packing list with your functions from forecast.py. Ready to use.
# Run it with: python trip.py            (asks the Weather Service, and falls back to the saved copy)
#          or: python trip.py --offline  (uses the saved copy without asking)
import argparse

import requests

from forecast import get_forecast, packing_list, weekend_periods


def no_network(url):
    """A stand-in fetch for --offline: it fails the way a lost connection does."""
    raise requests.exceptions.ConnectionError("--offline: not asking the Weather Service")


parser = argparse.ArgumentParser(description="Pine Ridge Campground's weekend forecast and packing list.")
parser.add_argument("--offline", action="store_true", help="use the saved copy instead of asking the Weather Service")
args = parser.parse_args()

if args.offline:
    forecast, source = get_forecast(fetch=no_network)
else:
    forecast, source = get_forecast()

periods = weekend_periods(forecast)
print(f"Pine Ridge Campground: this weekend ({source})")
for period in periods:
    print(f"  {period['name']}: {period['temperature']}°F, {period['rain_chance']}% chance of rain, {period['summary']}")
print("Pack:", ", ".join(packing_list(periods)))
