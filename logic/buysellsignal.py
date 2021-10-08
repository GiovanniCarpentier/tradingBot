from telegram_send import send


def sellSignal(prices):
    try:
        WMA = prices[0]
        SMA = prices[1]

        if WMA < SMA:
            return True
        else:
            return False
    except:
        send(messages=["ERROR while checking sell signal"])


def buySignal(prices):
    try:
        WMA = prices[0]
        RSI_K = prices[3]
        RSI_D = prices[4]
        SMA = prices[1]
        SUPERTREND = prices[6]

        AVG_RSI_VALUE = (RSI_K + RSI_D) / 2

        if WMA > SMA and RSI_K > RSI_D and AVG_RSI_VALUE < 50:
            return True
        elif WMA > SMA and RSI_K > RSI_D and SUPERTREND == "long":
            return True
        else:
            return False
    except:
        send(messages=["ERROR while checking buy signal"])

