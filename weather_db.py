import sqlite3
from datetime import datetime
import os


class WeatherStuff:
    def __init__(self):
        self.weathertest = "Addon_Functionality/WeatherControl/WeatherKeys.db"

    def tbl_check(self):
        if not os.path.isfile(self.weathertest):
            print(f"table doesn't exist yet")
            db = sqlite3.connect(self.weathertest)
            cur = db.cursor()

            cur.execute("CREATE TABLE IF NOT EXISTS weather_keys "
                        "('id' INTEGER PRIMARY KEY,"
                        "'City' text,"
                        "'State' text,"
                        "'Location_key' text,"
                        "'Last_Updated' text)")

            db.commit()
            cur.close()
            db.close()

            print("Weather Tables Created")

    def tbl_update(self, city, state, loc_key):

        db = sqlite3.connect(self.weathertest)
        cur = db.cursor()
        date_updated = str(datetime.now().year * 10000000000 +
                   datetime.now().month * 100000000 +
                   datetime.now().day * 1000000)[:-6]

        un_value = city, state, loc_key, date_updated

        cur.execute("INSERT INTO weather_keys VALUES (NULL, ?,?,?,?)", un_value)

        db.commit()
        cur.close()
        db.close()

    def pull_key(self, wcity,wstate):

        db = sqlite3.connect("Addon_Functionality/WeatherControl/WeatherKeys.db")
        cur = db.cursor()

        cur.execute("SELECT Location_key FROM weather_keys WHERE City = '" + wcity + "' AND State = '"
                    + wstate + "' LIMIT 1")

        getnum = len(cur.fetchall())
        key = cur.fetchone()
        if getnum == 1:
            print("We got the key!")
            return key
        else:
            return None
