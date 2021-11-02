from telegram_send import send


def sellSignal(prices):
    try:
        WMA = prices[0]
        VWMA = prices[1]

        send(messages=["WMA -> " + str(WMA) + " \n " +
             "VWMA -> " + str(VWMA)])

        if WMA <= VWMA:
            return True
        else:
            return False
    except:
        send(messages=["ERROR while checking sell signal"])


def buySignal(prices):
    try:
        WMA = prices[0]
        VWMA = prices[1]
        RSI = prices[3]

        send(messages=["WMA -> " + str(WMA) + " \n " +
             "VWMA -> " + str(VWMA) + " \n " + "RSI " + str(RSI)])

        if WMA >= VWMA and RSI < 70:
            return True
        else:
            return False
    except:
        send(messages=["ERROR while checking buy signal"])
