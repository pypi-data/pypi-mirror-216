# Currency API Python Package

The package provides convenient access to the [Currency API](https://moatsystems.com/currency-api/) functionality from applications written in the Python language.

## Requirements

Python 2.7 and later.

## Setup

You can install this package by using the pip tool and installing:

```python
pip install fxdatapi
## OR
easy_install fxdatapi
```

Install from source with:

```python
python setup.py install --user

## or `sudo python setup.py install` to install the package for all users
```

Usage Example
-------------

```python
from fxdatapi.auth import Auth
from fxdatapi.currencies import Currencies
from fxdatapi.historical import Historical
from fxdatapi.convert import Convert
from fxdatapi.convert_all import ConvertAll
from fxdatapi.daily_average import DailyAverage
from fxdatapi.weekly_average import WeeklyAverage
from fxdatapi.monthly_average import MonthlyAverage
from fxdatapi.margins_spreads import MarginsSpreads
from fxdatapi.performances import Performances
from fxdatapi.signals import Signals

# Authenticate and log in
auth = Auth()
username = "your_username"
password = "your_password"

result = auth.login(username, password)
print("Login successful:", result)

currencies = Currencies(auth.headers)
result = currencies.get_currencies(username, "19", "04", "2023")
print("Currencies:", result)

uuid = "currency_uuid"
result = currencies.get_currency(uuid, username, "19", "04", "2023")
print("Currency:", result)

historical = Historical(auth.headers)
result = historical.get_historical(username, "2023_04_19", "19", "04", "2023")
print("Historical data:", result)

uuid = "historical_uuid"
result = historical.get_historical_currency(uuid, username, "2023_04_19", "19", "04", "2023")
print("Historical currency:", result)

convert = Convert(auth.headers)
result = convert.convert_currency(username, "2023_04_19", "GBP", "EUR", "500")
print("Converted amount:", result)

convert_all = ConvertAll(auth.headers)
result = convert_all.convert_all_currencies(username, "GBP", 120, "2023_04_19")
print("Converted amounts:", result)

daily_average = DailyAverage(auth.headers)
result = daily_average.get_daily_average("2023_04_19")
print("Daily average:", result)

weekly_average = WeeklyAverage(auth.headers)
result = weekly_average.get_weekly_average("2023_04_03", "2023_04_07")
print("Weekly average:", result)

monthly_average = MonthlyAverage(auth.headers)
result = monthly_average.get_monthly_average("2023", "04")
print("Monthly average:", result)

margins_spreads = MarginsSpreads(auth.headers)
result = margins_spreads.get_margins_spreads(username, "19", "04", "2023")
print("Margins and spreads:", result)

uuid = "margins_spreads_uuid"
result = margins_spreads.get_margins_spreads_currency(uuid, username, "19", "04", "2023")
print("Margins and spreads for currency:", result)

performances = Performances(auth.headers)
result = performances.get_performances(username)
print("Performances:", result)

uuid = "performance_uuid"
result = performances.get_performance(uuid, username)
print("Performance:", result)

signals = Signals(auth.headers)
result = signals.get_signals(username)
print("Signals:", result)

uuid = "signal_uuid"
result = signals.get_signal(uuid, username)
print("Signal:", result)
```

## Setting up Currency API Account

Subscribe here for a [user account](https://moatsystems.com/currency-api/).


## Using the Currency API

You can read the [API documentation](https://docs.fxdatapi.com/) to understand what's possible with the Currency API. If you need further assistance, don't hesitate to [contact us](https://moatsystems.com/contact/).


## License

This project is licensed under the [BSD 3-Clause License](https://moatsystems.com/assets/license/BSD_3_Clause.txt).


## Copyright

(c) 2020 - 2023 [Moat Systems Limited](https://moatsystems.com/). All Rights Reserved.
