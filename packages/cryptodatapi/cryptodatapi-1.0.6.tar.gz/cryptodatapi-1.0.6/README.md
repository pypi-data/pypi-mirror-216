# Crypto API Python Package

The package provides convenient access to the [Crypto API](https://moatsystems.com/crypto-api/) functionality from applications written in the Python language.

## Requirements

Python 2.7 and later.

## Setup

You can install this package by using the pip tool and installing:

```python
pip install cryptodatapi
## OR
easy_install cryptodatapi
```

Install from source with:

```python
python setup.py install --user

## or `sudo python setup.py install` to install the package for all users
```

## Usage Example

```python
import cryptodatapi
from dotenv import load_dotenv
import os

## Loads environment variables from .env
load_dotenv('.env')

username = os.getenv('_USERNAME')
password = os.getenv('_PASSWORD')

## Authentication
cryptodatapi.login(username, password)

## Retrieve All Cryptocurrency Prices
cryptoPrices = cryptodatapi.get_crypto_price()
print(cryptoPrices)

## Retrieve Cryptocurrency Price by ID
cryptoPriceByID = cryptodatapi.get_crypto_price(id='<insert unique id>')
print(cryptoPriceByID)

## Retrieve Bitcoin Price
cryptoPrice = cryptodatapi.get_crypto_price(sym='BTC')
print(cryptoPrice)

## Retrieve All Cryptocurrency Top Gainers
cryptoGainers = cryptodatapi.get_gainers()
print(cryptoGainers)

## Retrieve Cryptocurrency Top Gainers by ID
cryptoGainersByID = cryptodatapi.get_gainers(id='<insert unique id>')
print(cryptoGainersByID)

## Retrieve All Cryptocurrency Top Losers
cryptoLosers = cryptodatapi.get_losers()
print(cryptoLosers)

## Retrieve Cryptocurrency Top Losers by ID
cryptoLosersByID = cryptodatapi.get_losers(id='<insert unique id>')
print(cryptoLosersByID)

## Retrieve All Cryptocurrency 2021 Historical Prices
cryptoHistorical2021 = cryptodatapi.get_hist_price_2021()
print(cryptoHistorical2021)

## Retrieve Cryptocurrency 2021 Historical Prices by ID
cryptoHistorical2021ByID = cryptodatapi.get_hist_price_2021(id='<insert unique id>')
print(cryptoHistorical2021ByID)

## Retrieve All Cryptocurrency 2022 Historical Prices
cryptoHistorical2022 = cryptodatapi.get_hist_price_2022()
print(cryptoHistorical2022)

## Retrieve Cryptocurrency 2022 Historical Prices by ID
cryptoHistorical2022ByID = cryptodatapi.get_hist_price_2022(id='<insert unique id>')
print(cryptoHistorical2022ByID)

## Retrieve All Cryptocurrency 2023 Historical Prices
cryptoHistorical2023 = cryptodatapi.get_hist_price_2023()
print(cryptoHistorical2023)

## Retrieve Cryptocurrency 2023 Historical Prices by ID
cryptoHistorical2023ByID = cryptodatapi.get_hist_price_2023(id='<insert unique id>')
print(cryptoHistorical2023ByID)

## Retrieve All Cryptocurrency Derivatives Exchanges
cryptoDerivatives = cryptodatapi.get_derivatives()
print(cryptoDerivatives)

## Retrieve Cryptocurrency Derivatives Exchanges by ID
cryptoDerivativesByID = cryptodatapi.get_derivatives(id='<insert unique id>')
print(cryptoDerivativesByID)

## Retrieve All Cryptocurrency Decentralized Exchanges
cryptoDecentralized = cryptodatapi.get_dex()
print(cryptoDecentralized)

## Retrieve Cryptocurrency Decentralized Exchanges by ID
cryptoDecentralizedByID = cryptodatapi.get_dex(id='<insert unique id>')
print(cryptoDecentralizedByID)

## Retrieve All Cryptocurrency Lending Exchanges
cryptoLending = cryptodatapi.get_lending()
print(cryptoLending)

## Retrieve Cryptocurrency Lending Exchanges by ID
cryptoLendingByID = cryptodatapi.get_lending(id='<insert unique id>')
print(cryptoLendingByID)

## Retrieve All Cryptocurrency Spot Exchanges
cryptoSpot = cryptodatapi.get_spot()
print(cryptoSpot)

## Retrieve Cryptocurrency Spot Exchanges by ID
cryptoSpotByID = cryptodatapi.get_spot(id='<insert unique id>')
print(cryptoSpotByID)

## Retrieve All Cryptocurrency News
cryptoNews = cryptodatapi.get_news()
print(cryptoNews)

## Retrieve Cryptocurrency News by ID
cryptoNewsByID = cryptodatapi.get_news(id='<insert unique id>')
print(cryptoNewsByID)
```

## Setting up a Crypto API Account

Sign up for a self-service [user account](https://moatsystems.com/crypto-api/).


## Using the MLS API

You can read the [API documentation](https://docs.cryptodatapi.com/) to understand what's possible with the MLS API. If you need further assistance, don't hesitate to [contact us](https://moatsystems.com/contact/).


## License

This project is licensed under the [MIT License](./LICENSE).


## Copyright

(c) 2020 - 2023 [Moat Systems Limited](https://moatsystems.com/). All Rights Reserved.
