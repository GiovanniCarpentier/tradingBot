import time
from logic.taapi import getData
from logic.buysellsignal import *
from telegram_send import send

START_MONEY = 1000
MONEY = 1000
WALLET = 0


def buyCheck(WALLET, MONEY):
    time.sleep(15)

    prices = getData()

    PRICE = prices[2]

    # Check for a buy logic
    if buySignal(prices):
        WALLET = float(round(MONEY / PRICE, 2))

        send(messages=["BOUGHT " + str(WALLET) + " XRP @ " + str(PRICE)])
        send(messages=["USDT SPENT " + str(MONEY)])

        sellCheck(WALLET, MONEY)
    else:
        buyCheck(WALLET, MONEY)


def sellCheck(WALLET, MONEY):
    time.sleep(16)

    prices = getData()

    PRICE = prices[2]

    # Check for a sell logic
    if sellSignal(prices):
        MONEY = float(round(WALLET * PRICE, 2))

        # Percentage Increase = (Increased Value - Original value) / Original value × 100

        PNL = (MONEY - START_MONEY) / START_MONEY * 100

        send(messages=["SOLD " + str(WALLET) + " XRP @ " + str(PRICE)])
        send(messages=["USDT BALANCE " + str(MONEY) + " TOTAL % GAINED " + str(round(PNL, 2)) + " %"])

        WALLET = 0
        buyCheck(WALLET, MONEY)
    else:
        sellCheck(WALLET, MONEY)


def startBot():
    buyCheck(WALLET, MONEY)


startBot()
