from crypto_com.cryptocom import *


def startBot():
    try:
        send(messages=["BOT is active"])
        if getBal("USDT") > getBal("XRP"):
            buyCheck()
        else:
            sellCheck()

    except:
        send(messages=["ERROR something went wrong while starting the bot"])


startBot()
