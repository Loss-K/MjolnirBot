import random
import sqlite3
from datetime import datetime
import os


class tablestuff:
    def __init__(self):
        self.ideasdb = "AddOn_Functionality/User_DB/Ideas.db"

    def tbl_check(self):
        if not os.path.isfile(self.ideasdb):
            print(f"table doesn't exist yet")
            db = sqlite3.connect(self.ideasdb)
            cur = db.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS ideas_database "
                        "('id' INTEGER PRIMARY KEY,"
                        "'datetime' int,"
                        "'User' text,"
                        "'msg' text)")

            db.commit()
            cur.close()
            db.close()

            print("Ideas Tables Created")
        else:
            print("Ideas Tables Exist")

    def tbl_update(self, user, msg_dtl):
        db = sqlite3.connect(self.ideasdb)
        cur = db.cursor()
        now2 = (datetime.now().year * 10000000000 +
                datetime.now().month * 100000000 +
                datetime.now().day * 1000000 +
                datetime.now().hour * 10000 +
                datetime.now().minute * 100 +
                datetime.now().second)

        un_value = now2, user, msg_dtl

        cur.execute("INSERT INTO ideas_database VALUES (NULL, ?,?,?)", un_value)

        db.commit()
        cur.close()
        db.close()

    def checkfirst(self,user, msg_dtl):
        if msg_dtl.lower().startswith('!idea'):
            msg_dtl = msg_dtl[6:]
        db = sqlite3.connect(self.ideasdb)
        print(self.ideasdb)
        cur = db.cursor()
        cur.execute("SELECT DISTINCT msg FROM ideas_database WHERE msg = '" +
                    str(msg_dtl) + "'")
        result = (cur.fetchall())

        if len(result) == 0:
            print(f"------- {user} with {msg_dtl}---------")
            # self.tbl_update(user, msg_dtl)
            tablestuff().tbl_update(user,msg_dtl)
            print("added")
        else:
            print("Idea already found. Not added")
