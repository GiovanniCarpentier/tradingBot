import mysql.connector
from telegram_send import send

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MQERsW4D",
    database="trades"
)


def insert(values):
    try:
        database = mydb.cursor()

        sql = "INSERT INTO trades (date, entry, exit, pnl, rsi) VALUES (%s, %s, %s, %s, %s)"
        val = values

        database.execute(sql, val)

        mydb.commit()
        send(messages=["Trade added to database"])
    except:
        send(messages=["ERROR while adding trade to database"])
