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
        "interval": "30m",
        "indicators": [
            {
                "indicator": "wma",
                "optInTimePeriod": 20
            },
            {
                "indicator": "vwma",
                "period": 37
            },
            {
                "indicator": "candle"
            },
            {
                "indicator": "rsi"
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
        prices.append(data[0]["result"]["value"])  # WMA // 0
        prices.append(data[1]["result"]["value"])  # VWMA // 1
        prices.append(data[2]["result"]["open"])  # PRICE // 2
        prices.append(data[3]["result"]["value"])  # RSI // 3

        return prices

    except Exception as e:
        send(messages=["ERROR while fetching TAAPI data"])
