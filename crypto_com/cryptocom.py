import hmac
import hashlib
import requests
import time
from telegram_send import send
from logic.buysellsignal import sellSignal, buySignal
from logic.taapi import getData

cryptoURL = "https://api.crypto.com/v2/"

API_KEY = "nEcxzHRgvLXLWdXThbQFxt"
SECRET_KEY = "xMZDDVMV36hvLc4gXwjo7Z"


def getBal(COIN):
    req = {
        "id": 11,
        "method": "private/get-account-summary",
        "api_key": API_KEY,
        "params": {
            "currency": COIN
        },
        "nonce": int(time.time() * 1000)
    }

    sig = digitalSignature(req)

    response = requests.post(cryptoURL + "private/get-account-summary", json=sig)

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
            "api_key": API_KEY,
            "params": {
                "instrument_name": "XRP_USDT",
                "side": SIDE,
                "type": TYPE,
                sort: float(round(getBal(COIN) - 0.1, 1))
            },
            "nonce": int(time.time() * 1000)
        }

        sig = digitalSignature(req)

        requests.post(cryptoURL + "private/create-order", json=sig)

        if SIDE == "BUY":
           sellCheck()
        else:
            send(messages=["USDT BALANCE " + str(getBal("USDT"))])
            buyCheck()
    except:
        send(messages=["ERROR while sending order to Crypto.com"])


def cancelAllOrders():
    try:
        req = {
            "id": 12,
            "method": "private/cancel-all-orders",
            "api_key": API_KEY,
            "params": {
                "instrument_name": "XRP_USDT",
            },
            "nonce": int(time.time() * 1000)
        }

        sig = digitalSignature(req)

        requests.post(cryptoURL + "private/cancel-all-orders", json=sig)

    except:
        send(messages=["ERROR while cancelling all orders"])


def stopLossActive():
    try:
        req = {
            "id": 12,
            "method": "private/get-open-orders",
            "api_key": API_KEY,
            "params": {
                "instrument_name": "XRP_USDT",
                "page_size": 1,
                "page": 0
            },
            "nonce": int(time.time() * 1000)
        }

        sig = digitalSignature(req)

        response = requests.post(cryptoURL + "private/get-open-orders", json=sig)

        DATA = response.json()

        if DATA["result"]["count"] < 1:
            STOPLOSS = open("stoploss.txt", "w")
            STOPLOSS.write("False")
            STOPLOSS.close()
            return False
        else:
            return True

    except:
        send(messages=["ERROR while checking if the stop loss is active"])


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
            FILE.write(PRICE)
            FILE.close()

            order("BUY", "USDT", "MARKET")

    except:
        send(messages=["ERROR while checking buy signal // Crypto.com"])


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

    except:
        send(messages=["ERROR while checking sell signal // Crypto.com"])


def checkForStopLossPlacement(prices):
    try:
        PRICES = prices[2]

        FILE = open("trade.txt", "r")
        ENTRY_PRICE = FILE.readline()
        FILE.close()

        # % = Diff ÷ Original Number × 100

        DIFFERENCE_PERCENTAGE = (float(ENTRY_PRICE) - PRICES) / float(ENTRY_PRICE) * 100

        if DIFFERENCE_PERCENTAGE > 10:
            STOPLOSS_PRICE = 0.05 * PRICES

            FILE = open("trade.txt", "w")
            FILE.write(STOPLOSS_PRICE)
            FILE.close()

            STOPLOSS = open("stoploss.txt", "w")
            STOPLOSS.write("True")
            STOPLOSS.close()

            cancelAllOrders()
            stopLoss("SELL", "XRP", "STOP_LOSS", STOPLOSS_PRICE)

        else:
            stopLossActive()

    except:
        send(messages=["ERROR while checking stop loss"])


def stopLoss(SIDE, COIN, TYPE, PRICE):
    try:
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
                "type": TYPE,
                "price": PRICE,
                sort: float(round(getBal(COIN) - 0.1, 1))
            },
            "nonce": int(time.time() * 1000)
        }

        sig = digitalSignature(req)

        response = requests.post(cryptoURL + "private/create-order", json=sig)

        send(messages=[str(response.json())])

    except:
        send(messages=["ERROR while sending order to Crypto.com"])


def digitalSignature(req):
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

    return req