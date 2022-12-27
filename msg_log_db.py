import random
import sqlite3
from datetime import datetime
import os


class tablestuff:
    def __init__(self):
        self.dbtest = "Twitch/Logs/Msg_Logs/MsgLog.db"

    def tbl_check(self):
        if not os.path.isfile(self.dbtest):
            print(f"table doesn't exist yet")
            db = sqlite3.connect(self.dbtest)
            cur = db.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS msg_detail "
                        "('id' INTEGER PRIMARY KEY,"
                        "'datetime' int,"
                        "'User' text,"
                        "'msg' text)")

            cur.execute("CREATE TABLE IF NOT EXISTS cmd_detail "
                        "('id' INTEGER PRIMARY KEY,"
                        "'datetime' int,"
                        "'User' text,"
                        "'command' text,"
                        "'command_detail' text)")

            db.commit()
            cur.close()
            db.close()

            print("Tables Created")

    def tbl_cleanup(self):
        db = sqlite3.connect(self.dbtest)
        cur = db.cursor()
        now2 = str(datetime.now().year * 10000000000 +
                   datetime.now().month * 100000000 +
                   datetime.now().day * 1000000)[:-6]

        cur.execute("DELETE FROM msg_detail WHERE datetime LIKE '" + str(now2) + "%'")

        db.commit()
        cur.close()
        db.close()

    def tbl_update(self, user, msg_dtl):
        db = sqlite3.connect(self.dbtest)
        cur = db.cursor()
        now2 = (datetime.now().year * 10000000000 +
                datetime.now().month * 100000000 +
                datetime.now().day * 1000000 +
                datetime.now().hour * 10000 +
                datetime.now().minute * 100 +
                datetime.now().second)

        un_value = now2, user, msg_dtl

        cur.execute("INSERT INTO msg_detail VALUES (NULL, ?,?,?)", un_value)

        db.commit()

    def cmd_update(self, user, cmd_name, cmd_dtl):
        # db = sqlite3.connect(self.dbtest)
        # cur = db.cursor()
        # now2 = (datetime.now().year * 10000000000 +
        #         datetime.now().month * 100000000 +
        #         datetime.now().day * 1000000 +
        #         datetime.now().hour * 10000 +
        #         datetime.now().minute * 100 +
        #         datetime.now().second)
        #
        # un_value = now2, user, cmd_name, cmd_dtl
        # cur.execute("INSERT INTO cmd_detail VALUES (NULL, ?,?,?,?)", un_value)
        #
        # db.commit()

        pass

        #print(f"inserted: {str(now2)}, {str(user)}, {str(cmd_name)}, {str(cmd_dtl)}")

    def pick_random(self):
        db = sqlite3.connect("Twitch/Logs/Msg_Logs/MsgLog.db")
        cur = db.cursor()

        now2 = str(datetime.now().year * 10000000000 +
                   datetime.now().month * 100000000 +
                   (datetime.now().day - 1) * 1000000)[:-6]

        print(now2)
        #cur.execute("SELECT * FROM msg_detail WHERE datetime LIKE '" + str(now2) + "%'")
        cur.execute("SELECT DISTINCT User FROM msg_detail WHERE datetime LIKE '" + str(now2) + "%'")
        getnum = len(cur.fetchall())

        #tcur.execute("SELECT * FROM msg_detail ORDER BY datetime DESC LIMIT 1")

        getlast = len(cur.fetchall())
        print(getnum)
        print(getlast)


        if getnum < 2:
            print("Theres only one person to pick in the log.")
            target = "the stars above"
            return target
        else:

            result = random.randrange(1, getnum)
            print(result)
            target = cur.execute("SELECT User FROM msg_detail WHERE id = " + str(result)).fetchone()
            target = str(target)
            target = target[2:-3]
            return "@" + target


    def confirmstate(self):

        list_of_States = []
        States_Abbrev = []

        print("Whee")