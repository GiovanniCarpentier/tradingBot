import requests

# SECRET KEY TAAPI eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ikdpb3Zhbm5pY2FycGVudGllckBvdXRsb29rLmNvbSIsImlhdCI6MTYzMjkwMDkzNSwiZXhwIjo3OTQwMTAwOTM1fQ.XFN1Mwc6Y8-sNbWdbEbheVzB2V-aamh1eZ38g8CFncQ
from telegram_send import send


endpoint = "https://api.taapi.io/bulk"

parameters = {
    "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ikdpb3Zhbm5pY2FycGVudGllckBvdXRsb29rLmNvbSIsImlhdCI6MTYzMjkwMDkzNSwiZXhwIjo3OTQwMTAwOTM1fQ.XFN1Mwc6Y8-sNbWdbEbheVzB2V-aamh1eZ38g8CFncQ",
    "construct": {
        "exchange": "binance",
        "symbol": "XRP/USDT",
        "interval": "1h",
        "indicators": [
            {
                "indicator": "wma",
                "optInTimePeriod": 26
            },
            {
                "indicator": "vwma",
                "period": 40
            },
            {
                "indicator": "candle"
            },
            {
                "indicator":"rsi"
            }
        ]
    }
}


def getData():
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
