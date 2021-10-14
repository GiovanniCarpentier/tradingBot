from telegram_send import send


def sellSignal(prices):
    try:
        WMA = prices[0]
        VWMA = prices[1]

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

        if WMA >= VWMA and RSI < 70:
            return True
        else:
            return False
    except:
        send(messages=["ERROR while checking buy signal"])
