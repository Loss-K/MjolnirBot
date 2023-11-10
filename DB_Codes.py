import random
import sqlite3
from datetime import datetime
import os


class tablestuff:
    def __init__(self):
        self.dbtest = "Logs/DB_Name.db"

    def cur_action(self):
        pass


    def tbl_check(self):
        if not os.path.isfile(self.dbtest):
            print(f"The logging DB doesn't exist for the user yet.")
            db = sqlite3.connect(self.dbtest)
            cur = db.cursor()

            #Create a Log of Twitch Bot Users, their Twitch ID, Discord ID(?)
            # to reduce number of calls for the information and for easy reconnection if the bot has to restart.
            # We need to check if we can hold that data, and for how long if so.
            cur.execute("CREATE TABLE IF NOT EXISTS bot_approved_users "
                        "('id' INTEGER PRIMARY KEY,"
                        "'User' text,"
                        "'DiscordID' text,"
                        "'TwitchID' text)")

            #Create a Log of Users, their Twitch ID, Discord ID(?) to reduce number of calls for the information.
            # We need to check if we can hold that data, and for how long if so.
            # and how often they spammed or cussed in Discord.
            cur.execute("CREATE TABLE IF NOT EXISTS user_detail "
                        "('id' INTEGER PRIMARY KEY,"
                        "'User' text,"
                        "'DiscordID' text,"
                        "'TwitchID' text,"
                        "'CussHistory' int,"
                        "'SpamHistory' int)")

            #Creates message Tables - This will allow tracking of messages for Twitch Streams
            cur.execute("CREATE TABLE IF NOT EXISTS twitch_msg_detail "
                        "('id' INTEGER PRIMARY KEY,"
                        "'datetime' int,"
                        "'User' text,"
                        "'msg' text)")

            # Creates message Tables - This will allow tracking of messages for Discord Streams.
            cur.execute("CREATE TABLE IF NOT EXISTS discord_msg_detail "
                        "('id' INTEGER PRIMARY KEY,"
                        "'datetime' int,"
                        "'User' text,"
                        "'msg' text)")

            #Creates a Table for Commands not found - This will allow owners to determine future needs.
            cur.execute("CREATE TABLE IF NOT EXISTS cmd_detail "
                        "('id' INTEGER PRIMARY KEY,"
                        "'datetime' int,"
                        "'User' text,"
                        "'command' text,"
                        "'command_detail' text)")

            # Creates a table for future ideas -> !idea on Twitch or /idea on Discord (In Progress)
            #### Need to update idea code for origin field addition ####
            cur.execute("CREATE TABLE IF NOT EXISTS ideas_database "
                        "('id' INTEGER PRIMARY KEY,"
                        "'datetime' int,"
                        "'User' text,"
                        "'msg' text,"
                        "'origin', text)")

            # Creates a table for the API Call via Accuweather. As Keys get collected, it'll store them to reduce
            # the number of calls in the future

            cur.execute("CREATE TABLE IF NOT EXISTS weather_keys "
                        "('id' INTEGER PRIMARY KEY,"
                        "'City' text,"
                        "'State' text,"
                        "'Location_key' text,"
                        "'Last_Updated' text)")

            ## Creates Command Tables to add and manage custom commands.

            cur.execute("CREATE TABLE IF NOT EXISTS custom_commands "
                        "('id' INTEGER PRIMARY KEY,"
                        "'command_name' text,"
                        "'Command_line' text,"
                        "'Date_Added' text,"
                        "'Last_Updated' text)")

            db.commit()
            cur.close()
            db.close()

            print("Tables Created")

    # Check Action to do, then do action type based on the table that needs to update.
    def tbl_record_action(self, table_to_update, action_type, criteria):
        now2 = (datetime.now().year * 10000000000 +
                datetime.now().month * 100000000 +
                datetime.now().day * 1000000 +
                datetime.now().hour * 10000 +
                datetime.now().minute * 100 +
                datetime.now().second)


        if action_type == 'add':
            action_sign = "+"
        elif action_type == 'remove':
            action_type = "-"
        elif action_type == 'change':
            action_type = "wat do I put here"

        ## Just a reference

        un_value = table_to_update, criteria, action_sign

        #cur.execute("INSERT INTO msg_detail VALUES (NULL, ?,?,?)", un_value)

        match table_to_update:
            case "BTUSER":
                pass
            case "UserDetail":
                # If user is already in the table...
                # If user is not already in the table, Add them first.
                # Part two is to update the record.
                # May want to move this outside match to see if they exist PRIOR to any calls then match future tables.
                pass
            case "MSGUSER-Twitch":
                pass
            case "MSGUSER-Discord":
                pass
            case "unknown_commands":
                pass
            case "ideas":
                pass
            case "weather":
                pass

