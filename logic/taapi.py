import requests
import os

from telegram_send import send
from dotenv import load_dotenv

load_dotenv()

endpoint = "https://api.taapi.io/bulk"

parameters = {
    "secret": os.getenv("SECRET"),
    "construct": {
        "exchange": "binance",
        "symbol": "XRP/USDT",
        "interval": "5m",
        "indicators": [
            {
                "indicator": "rsi",
                "optInTimePeriod": 14
            },
            {
                "indicator": "sma",
                "period": 100
            },
            {
                "indicator": "candle"
            }
        ]
    }
}


def getData():
    try:
        # Send request to TAAPI and save it to response
        response = requests.post(url=endpoint, json=parameters)

        # Get the response JSON
        result = response.json()

        # Create empty array to store price data
        prices = []

        # Get the data from the JSON
        data = result.get("data")

        # For every item in data get the result and the value in the result and add it to the price array
        prices.append(data[0]["result"]["value"])  # RSI
        prices.append(data[1]["result"]["value"])  # SMA
        prices.append(data[2]["result"]["close"])  # PRICE // 2

        return prices

    except Exception as e:
        send(messages=["ERROR while fetching TAAPI data"])
