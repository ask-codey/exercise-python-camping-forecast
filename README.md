# Exercise: Camping Trip Forecast

Exercise code for the lesson **Exercise: Camping Trip Forecast** in the Python in Depth course on [ask-codey.com](https://www.ask-codey.com).

A weekend at Pine Ridge Campground needs a forecast and a packing list. You'll write the four functions in `forecast.py` that get them from the US National Weather Service's API: find the forecast's address in the point's answer, pick out the weekend's periods, plan what to pack, and fall back to a saved copy when the network is down. The tests check each function without ever touching the network.

Pine Ridge Campground is made up; its coordinates (44.8783, -122.6534) are a real state park's in Oregon, so the forecast is real. The Weather Service's data is free to use, and it needs no key.

## What's here

- `forecast.py`: `fetch_json` (ready to use: it asks the Weather Service for an address and returns the JSON answer), and the four functions `forecast_url`, `weekend_periods`, `packing_list` and `get_forecast`. Each of the four stops with `NotImplementedError: Not built yet.` for now. The docstring under each says what it should return, with examples. For you to finish.
- `trip.py`: prints the weekend's forecast and packing list with your functions, so you can see them at work. Ready to use.
- `saved/points.json` and `saved/forecast.json`: the Weather Service's real answers for the campground, saved on 2026-11-17. The tests read them. Ready to use.
- `saved/forecast-copy.json`: the saved copy `get_forecast` falls back to, dated 2026-11-17. Each time `get_forecast` gets a live forecast, it replaces this file with the new one and today's date.
- `tests/test_forecast.py`: tests that call your functions and check what comes back. You don't need to change this file.
- `requirements.txt`: the packages the exercise needs, pytest and requests, at exact versions. Ready to use.
- `pytest.ini`: tells pytest where the tests are and where to find `forecast.py`. Ready to use.
- `.gitignore`: tells Git to leave out the virtual environment and the files Python and pytest make as they run. Ready to use.

## Before you start

The tests need pytest, and `forecast.py` needs requests, so both go in a virtual environment: a private set of packages for this folder only. In VS Code's terminal, in this folder, run these three commands.

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On a Mac (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- The first command makes the virtual environment, in a folder named `.venv`.
- The second turns it on for this terminal: the prompt starts with `(.venv)` from then on.
- The third installs the packages `requirements.txt` lists into it: pytest and requests.

*Virtual Environments and pip*, in Module 3, explains all three. The `.venv` folder is in `.gitignore`, so Git leaves it out: these commands make it again on any computer.

If PowerShell answers that running scripts is disabled on this system, run this once, then run the second command again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Each new terminal starts with the virtual environment off. If the prompt doesn't start with `(.venv)`, run the second command again. (VS Code often turns it on for you.)

## Check your work

```bash
pytest
```

At first every test fails: that is expected, because each function stops with a `NotImplementedError` for now. Each function you finish turns its tests green. A failing test's message says what it called, what it expected and what came back, for example *forecast_url(saved points.json) should return 'https://api.weather.gov/gridpoints/PQR/107,74/forecast', but it returned None.* The tests work offline: they never ask the Weather Service.

To see your functions at work, run:

```bash
python trip.py --offline
```

That uses the saved copy. `python trip.py`, without `--offline`, asks the Weather Service for this weekend's real forecast, and falls back to the saved copy if it can't.

## The rules

- Keep each function's name and parameters as they are, and keep `fetch_json`, `POINTS_URL`, `HEADERS`, `WEEKEND` and `SAVED_COPY` as they are.
- Return each answer; don't print it. The tests read what your functions return.
- `get_forecast` asks for data only through its `fetch` parameter, never with `requests.get` directly: that's how the tests hand it stand-ins.
- Don't change the tests, `trip.py`, `saved/points.json` or `saved/forecast.json`. (`get_forecast` updates `saved/forecast-copy.json` itself.)

## Tips

- Open `saved/points.json` and `saved/forecast.json` in VS Code and find the values each docstring names before you write any code.
- Follow the keys from the outside in: `points_json["properties"]` first, then the key inside it.
- `weekend_periods` builds a new list: start with an empty one and `append` a small dictionary for each weekend period.
- "Any period" means checking every period in a loop. A variable that starts as `False` and turns `True` when one period matches remembers it for after the loop.
- In `get_forecast`, put both `fetch` calls in the `try` block, and catch `requests.exceptions.RequestException`, the parent of every error a request can raise.

## Hand it in

When it works, push your solution to a public repo of your own on GitHub, then paste that repo's address into **Submit your exercise** on the lesson page at [ask-codey.com](https://www.ask-codey.com). That's what completes the lesson. The lesson page shows the Git commands, step by step.
