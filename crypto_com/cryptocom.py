import hmac
import hashlib
import requests
import time
from telegram_send import send
from logic.buysellsignal import sellSignal, buySignal
from logic.taapi import getData

cryptoURL = "https://api.crypto.com/v2/"

API_KEY = ""
SECRET_KEY = ""


def getBal(COIN):
    NONCE = int(time.time() * 1000)

    req = {
        "id": 11,
        "method": "private/get-account-summary",
        "api_key": API_KEY,
        "params": {
            "currency": COIN
        },
        "nonce": NONCE
    }

    # First ensure the params are alphabetically sorted by key
    paramString = ""

    if "params" in req:
        for key in sorted(req['params']):
            paramString += key
            paramString += str(req['params'][key])

    sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])

    req['sig'] = hmac.new(
        bytes(str(SECRET_KEY), 'utf-8'),
        msg=bytes(sigPayload, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    response = requests.post(cryptoURL + "private/get-account-summary", json=req)

    result = response.json()

    account = result["result"]["accounts"][0]["available"]

    return account


def order(SIDE, COIN):
    try:
        NONCE = int(time.time() * 1000)

        if SIDE == "BUY":
            sort = "notional"
        else:
            sort = "quantity"

        req = {
            "id": 11,
            "method": "private/create-order",
            "api_key": API_KEY,
            "params": {
                "instrument_name": "XRP_USDT",
                "side": SIDE,
                "type": "MARKET",
                sort: float(round(getBal(COIN), 1) - 0.1)
            },
            "nonce": NONCE
        }

        # First ensure the params are alphabetically sorted by key
        paramString = ""

        if "params" in req:
            for key in sorted(req['params']):
                paramString += key
                paramString += str(req['params'][key])

        sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])

        req['sig'] = hmac.new(
            bytes(str(SECRET_KEY), 'utf-8'),
            msg=bytes(sigPayload, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        requests.post(cryptoURL + "private/create-order", json=req)

        if SIDE == "BUY":
           sellCheck()
        else:
            send(messages=["USDT BALANCE " + str(getBal("USDT"))])
            buyCheck()
    except:
        send(messages=["ERROR while sending order to Crypto.com"])


def buyCheck():
    try:
        time.sleep(16)

        prices = getData()
        PRICE = prices[2]

        if buySignal(prices):
            WALLET = getBal("USDT") / PRICE

            # SEND TO TELEGRAM
            send(messages=["BOUGHT " + str(WALLET) + " XRP @ " + str(PRICE)])
            send(messages=["USDT SPENT " + str(WALLET)])

            order("BUY", "USDT")

        else:
            buyCheck()
    except:
        send(messages=["ERROR while checking checking buy signal"])


def sellCheck():
    try:
        time.sleep(16)

        prices = getData()
        PRICE = prices[2]

        if sellSignal(prices):
            WALLET = getBal("XRP")

            # SEND MESSAGE TO TELEGRAM
            send(messages=["SOLD " + str(WALLET) + " XRP @ " + str(PRICE)])
            order("SELL", "XRP")

        else:
            sellCheck()

    except:
        send(messages=["ERROR while checking sell signal"])

