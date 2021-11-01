import hmac
import hashlib
import requests
import time
import os

from telegram_send import send
from logic.buysellsignal import sellSignal, buySignal
from logic.taapi import getData
from dotenv import load_dotenv

cryptoURL = "https://api.crypto.com/v2/"

load_dotenv()


def getBal(COIN):
    req = {
        "id": 11,
        "method": "private/get-account-summary",
        "api_key": os.getenv("API_KEY"),
        "params": {
            "currency": COIN
        },
        "nonce": int(time.time() * 1000)
    }

    sig = digitalSignature(req)

    response = requests.post(
        cryptoURL + "private/get-account-summary", json=sig)

    result = response.json()

    account = result["result"]["accounts"][0]["available"]

    return account


def order(SIDE, COIN, TYPE):
    try:
        if SIDE == "BUY":
            sort = "notional"
        else:
            sort = "quantity"

        req = {
            "id": 11,
            "method": "private/create-order",
            "api_key": os.getenv("API_KEY"),
            "params": {
                "instrument_name": "XRP_USDT",
                "side": SIDE,
                "type": TYPE,
                sort: float(round(getBal(COIN) - 1, 1))
            },
            "nonce": int(time.time() * 1000)
        }

        sig = digitalSignature(req)

        response = requests.post(cryptoURL + "private/create-order", json=sig)

        send(messages=[str(response.json())])

        if SIDE == "SELL":
            send(messages=["USDT BALANCE " + str(getBal("USDT"))])
    except Exception as e:
        send(messages=["ERROR while sending order to Crypto.com"])
        print(e)


def cancelAllOrders():
    try:
        req = {
            "id": 12,
            "method": "private/cancel-all-orders",
            "api_key": os.getenv("API_KEY"),
            "params": {
                "instrument_name": "XRP_USDT",
            },
            "nonce": int(time.time() * 1000)
        }

        sig = digitalSignature(req)

        requests.post(cryptoURL + "private/cancel-all-orders", json=sig)

    except Exception as e:
        send(messages=["ERROR while cancelling all orders"])
        print(e)


def stopLossActive():
    try:
        req = {
            "id": 12,
            "method": "private/get-open-orders",
            "api_key": os.getenv("API_KEY"),
            "params": {
                "instrument_name": "XRP_USDT",
                "page_size": 1,
                "page": 0
            },
            "nonce": int(time.time() * 1000)
        }

        sig = digitalSignature(req)

        response = requests.post(
            cryptoURL + "private/get-open-orders", json=sig)

        DATA = response.json()

        FILE = open("stoploss.txt", "r")
        stoploss = FILE.readline()

        if stoploss == "":
            return True
        elif DATA["result"]["count"] < 1:
            STOPLOSS = open("stoploss.txt", "w")
            STOPLOSS.write("False")
            STOPLOSS.close()
            return False
        else:
            return True

    except Exception as e:
        send(messages=["ERROR while checking if the stop loss is active"])
        print(e)


def checkForStopLossPlacement(prices):
    try:
        PRICES = prices[2]

        FILE = open("trade.txt", "r")
        ENTRY_PRICE = FILE.readline()
        FILE.close()

        # % = Diff ÷ Original Number × 100

        DIFFERENCE_PERCENTAGE = (
            PRICES - float(ENTRY_PRICE)) / float(ENTRY_PRICE) * 100

        print(DIFFERENCE_PERCENTAGE)

        if DIFFERENCE_PERCENTAGE > 10:
            STOPLOSS_PRICE = 0.05 * float(PRICES)

            print(STOPLOSS_PRICE)

            FILE = open("trade.txt", "w")
            FILE.write(str(STOPLOSS_PRICE))
            FILE.close()

            STOPLOSS = open("stoploss.txt", "w")
            STOPLOSS.write("True")
            STOPLOSS.close()

            cancelAllOrders()
            stopLoss("SELL", "XRP", "STOP_LOSS", STOPLOSS_PRICE)

        else:
            stopLossActive()

    except Exception as e:
        send(messages=["ERROR while checking stop loss"])
        print(e)


def stopLoss(SIDE, COIN, TYPE, PRICE):
    try:
        if SIDE == "BUY":
            sort = "notional"
        else:
            sort = "quantity"

        req = {
            "id": 11,
            "method": "private/create-order",
            "api_key": os.getenv("API_KEY"),
            "params": {
                "instrument_name": "XRP_USDT",
                "side": SIDE,
                "type": TYPE,
                "trigger_price": PRICE,
                sort: float(round(getBal(COIN) - 1, 1))
            },
            "nonce": int(time.time() * 1000)
        }

        print(req)

        sig = digitalSignature(req)

        response = requests.post(cryptoURL + "private/create-order", json=sig)

        send(messages=["Placed stop loss"])
        send(messages=[str(response.json())])

    except Exception as e:
        send(messages=["ERROR while sending order to Crypto.com"])
        print(e)


def buyCheck():
    try:
        time.sleep(16)

        prices = getData()
        PRICE = prices[2]

        if buySignal(prices):
            BAL = getBal("USDT")
            WALLET = BAL / PRICE

            # SEND TO TELEGRAM
            send(messages=["BOUGHT " + str(WALLET) + " XRP @ " + str(PRICE)])
            send(messages=["USDT SPENT " + str(BAL)])

            FILE = open("trade.txt", "w")
            FILE.write(str(PRICE))
            FILE.close()

            order("BUY", "USDT", "MARKET")

    except Exception as e:
        send(messages=["ERROR while checking buy signal // Crypto.com"])
        print(e)


def sellCheck():
    try:
        time.sleep(16)

        prices = getData()
        PRICE = prices[2]

        if sellSignal(prices):
            WALLET = getBal("XRP")

            # SEND MESSAGE TO TELEGRAM
            send(messages=["SOLD " + str(WALLET) + " XRP @ " + str(PRICE)])
            order("SELL", "XRP", "MARKET")

        else:
            checkForStopLossPlacement(prices)

    except Exception as e:
        send(messages=["ERROR while checking sell signal // Crypto.com"])
        print(e)


def digitalSignature(req):
    paramString = ""

    if "params" in req:
        for key in sorted(req['params']):
            paramString += key
            paramString += str(req['params'][key])

    sigPayload = req['method'] + str(req['id']) + \
        req['api_key'] + paramString + str(req['nonce'])

    req['sig'] = hmac.new(
        bytes(str(os.getenv("SECRET_KEY")), 'utf-8'),
        msg=bytes(sigPayload, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    return req
