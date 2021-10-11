from crypto_com.cryptocom import *


def checkForStopLoss():
    FILE = open("stoploss.txt", "r")
    stoploss = FILE.readline()
    return stoploss


def startBot():
    try:
        if checkForStopLoss() == "False":
            if sellSignal(getData()):
                FILE = open("stoploss.txt", "w")
                FILE.write("")
        else:
            if getBal("USDT") > getBal("XRP"):
                buyCheck()
            else:
                sellCheck()

    except:
        send(messages=["ERROR something went wrong while starting the bot"])


startBot()
