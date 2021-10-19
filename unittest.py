from crypto_com.cryptocom import *
from logic.buysellsignal import *
from logic.taapi import *


def testGetData():
    data = getData()
    print(data)
    return data


def testSellSignal(prices):
    print(sellSignal(prices))
    print("done")


def testBuySignal(prices):
    print(buySignal(prices))
    print("done")


def testGetBal():
    print(getBal("USDT"))
    print("done")


def testCancelOrders():
    # Create open order on crypto.com to test this function
    cancelAllOrders()
    print("done")


def testOrder(SIDE, COIN, TYPE):
    order(SIDE, COIN, TYPE)
    print("done")


def testStopLossActive():
    print(stopLossActive())
    print("done")


def testCheckForStopLossPlacement(prices):
    checkForStopLossPlacement(prices)
    print("done")


def testStopLoss(SIDE, COIN, TYPE, PRICE):
    stopLoss(SIDE, COIN, TYPE, PRICE)
    print("done")


def testBuyCheck():
    buyCheck()
    print("done")


def testSellCheck():
    sellCheck()
    print("done")


def startTesting():
    data = testGetData()

    time.sleep(10)

    testSellSignal(data)

    time.sleep(5)

    testBuySignal(data)

    time.sleep(5)

    testGetBal()

    time.sleep(5)

    testBuyCheck()

    time.sleep(5)

    testSellCheck()

    time.sleep(5)

    testCancelOrders()

    time.sleep(5)

    testOrder("BUY", "USDT", "MARKET")

    time.sleep(5)

    testCheckForStopLossPlacement(data)

    time.sleep(5)

    testStopLossActive()

    time.sleep(5)

    testStopLoss("SELL", "XRP", "STOPLOSS", 1)


startTesting()
