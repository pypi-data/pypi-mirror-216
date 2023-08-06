# MLS API Python Package

The package provides convenient access to the [MLS API](https://moatsystems.com/mls-api/) functionality from applications written in the Python language.

## Requirements

Python 2.7 and later.

## Setup

You can install this package by using the pip tool and installing:

```python
pip install mls-api
## OR
easy_install mls-api
```

Install from source with:

```python
python setup.py install --user

## or `sudo python setup.py install` to install the package for all users
```

Usage Example
-------------

```python
import mls_api
from dotenv import load_dotenv
import os

## Loads environment variables from .env
load_dotenv('.env')

username = os.getenv('_USERNAME')
password = os.getenv('_PASSWORD')

## Authentication
mls_api.login(username, password)

## Retrieve MLS Real-Time Data
mls_rtd = mls_api.get_rtd()
print(mls_rtd)

## Retrieve MLS Historical Data
mls_historical = mls_api.get_historical_data()
print(mls_historical)

## Retrieve MLS Players Data
limit = 5
offset = 5

mls_players_l = mls_api.get_players(limit=limit)
print(mls_players_l)

mls_players = mls_api.get_players(limit=limit, offset=offset)
print(mls_players)

## Retrieve MLS Assist Data
mls_assists = mls_api.get_assists()
print(mls_assists)

## Retrieve MLS Offence Data
mls_offence = mls_api.get_offence()
print(mls_offence)

## Retrieve MLS Top Scorers Data
mls_top_scorer = mls_api.get_top_scorer()
print(mls_top_scorer)

## Retrieve MLS Teams Data
mls_teams = mls_api.get_teams()
print(mls_teams)

## Retrieve MLS Fixtures Data
mls_fixtures = mls_api.get_fixtures()
print(mls_fixtures)

## Retrieve MLS Standings Data
mls_standings = mls_api.get_standings()
print(mls_standings)

## Retrieve MLS Latest News Data
mls_latest_news = mls_api.get_latest_news()
print(mls_latest_news)
```

## Setting up an MLS API Account

Sign up for a self-service [user account](https://moatsystems.com/mls-api/).


## Using the MLS API

You can read the [API documentation](https://docs.mlssoccerapi.com/) to understand what's possible with the MLS API. If you need further assistance, don't hesitate to [contact us](https://moatsystems.com/contact/).


## License

This project is licensed under the [MIT License](./LICENSE).


## Copyright

(c) 2021 - 2023 [Moat Systems Limited](https://moatsystems.com/). All Rights Reserved.
