import sqlite3
from datetime import datetime
import os


class tablestuff:
    def __init__(self):
        dbtest = "MsgLog.db"

    def tbl_update(self, user, text, err_status="False", bot_msg_status="False"):
        db = sqlite3.connect("MsgLog.db")
        cur = db.cursor()
        now2 = (datetime.now().year * 10000000000 +
                datetime.now().month * 100000000 +
                datetime.now().day * 1000000 +
                datetime.now().hour * 10000 +
                datetime.now().minute * 100 +
                datetime.now().second)

        cur.execute("INSERT INTO msg_detail(datetime,User,Message,Err_msg,Bot_Msg) "
                    "VALUES ('" + str(now2) + "','" + str(user) + "','" + str(text) + "','" + str(err_status) +
                    "'," + str(bot_msg_status) + ")")
        db.commit()
        print("Did a thing")

    def checktableexists(self):
        if not os.path.isfile("MsgLog.db"):
            db = sqlite3.connect("MsgLog.db")
            cur = db.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS msg_detail "
                        "('id' INTEGER PRIMARY KEY,"
                        "'datetime' int,"
                        "'User' text,"
                        "'Message' test,"
                        "'Err_msg' boolean,"
                        "'Bot_msg' boolean)")

            db.commit()
            cur.close()
            db.close()


tablestuff.checktableexists(0)
tablestuff.tbl_update(0, "dmatru", "hello")
