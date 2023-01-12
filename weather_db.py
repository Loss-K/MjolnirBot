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


    #
    # def confirmstate(self):
    #     #Saving - goal is to do a simple if statement that if the full name is searched, to use the abbrev
    #     # for the states. Its simple, but for another day.
    #
    #     #list_of_States = [Alabama, Alaska, Arizona, Arkansas, American Samoa, California, Colorado, Connecticut,
    #     # Delaware, District of Columbia, Florida, Georgia, Guam, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas,
    #     # Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana,
    #     # Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota,
    #     # Northern Mariana Islands, Ohio, Oklahoma, Oregon, Pennsylvania, Puerto Rico, Rhode Island, South Carolina,
    #     # South Dakota, Tennessee, Texas, Trust Territories, Utah, Vermont, Virginia, Virgin Islands, Washington,
    #     # West Virginia, Wisconsin, Wyoming]
    #
    #     #States_Abbrev = [AL, AK, AZ, AR, AS, CA, CO, CT, DE, DC, FL, GA, GU, HI, ID, IL, IN, IA, KS, KY, LA, ME, MD,
    #     # MA, MI, MN, MS, MO, MT, NE, NV, NH, NJ, NM, NY, NC, ND, MP, OH, OK, OR, PA, PR, RI, SC, SD, TN, TX, TT, UT,
    #     # VT, VA, VI, WA, WV, WI, WY]
    #
    #     print("Whee")