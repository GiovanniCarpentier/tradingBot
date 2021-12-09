from telegram_send import send


def sellSignal(prices):
    try:
        RSI = prices[0]

        if RSI > 75:
            return True
        else:
            return False
    except:
        send(messages=["ERROR while checking sell signal"])


def buySignal(prices):
    try:
        RSI = prices[0]
        SMA = prices[1]
        CANDLE = prices[3]

        if CANDLE > SMA and RSI < 75:
            return True
        else:
            return False
    except:
        send(messages=["ERROR while checking buy signal"])
