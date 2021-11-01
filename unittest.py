from crypto_com.cryptocom import *
from logic.buysellsignal import *
from logic.taapi import *

"""""
def testGetData():
    print("start get data")
    data = getData()
    print(data)
    return data


def testSellSignal(prices):
    print("start test sell signal")
    print(sellSignal(prices))
    print("done")


def testBuySignal(prices):
    print("start test buy signal")
    print(buySignal(prices))
    print("done")


def testGetBal():
    print("start test get balance")
    print(getBal("USDT"))
    print("done")


def testCancelOrders():
    print("start test cancel all orders")
    # Create open order on crypto.com to test this function
    cancelAllOrders()
    print("done")


"""


def testOrder(SIDE, COIN, TYPE):
    print("start test order")
    order(SIDE, COIN, TYPE)
    print("done")


"""

def testStopLossActive():
    print("start test stop loss active")
    print(stopLossActive())
    print("done")


def testCheckForStopLossPlacement(prices):
    print("start test stop loss placement")
    checkForStopLossPlacement(prices)
    print("done")


def testStopLoss(SIDE, COIN, TYPE, PRICE):
    print("start test stop loss")
    stopLoss(SIDE, COIN, TYPE, PRICE)
    print("done")


def testBuyCheck():
    print("start test buy check")
    buyCheck()
    print("done")


def testSellCheck():
    print("start test sell check")
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
"""

testOrder("SELL", "XRP", "MARKET")

time.sleep(10)

testOrder("BUY", "USDT", "MARKET")
