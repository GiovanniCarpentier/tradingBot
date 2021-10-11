import mysql.connector
from telegram_send import send

mydb = mysql.connector.connect(
    host="localhost",
    user="acer",
    password="acer",
    database="trades"
)

def select():
    database = mydb.cursor()

    sql = "SELECT * FROM trades"

    database.execute(sql)

    result = database.fetchall()

    print(result)



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


select()