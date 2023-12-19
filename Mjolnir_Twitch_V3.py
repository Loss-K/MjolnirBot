from twitchio.ext import commands
import Ideas_DB
import random
import requests
import os
import sqlite3
import weather_db

with open("./Config/Secret", "r") as f:
    lines = f.readlines()
    code1 = str.lower(lines[0]).strip()
    code2 = str.lower(lines[1]).strip()
    code3 = str.lower(lines[2]).strip()
    code4 = str.lower(lines[3]).strip()
    wcode = str(lines[5]).strip()
    Dmatru_token = str(lines[8]).strip()

PREFIX = "!"


class Mjolnirbot(commands.Bot):

    def __init__(self):

        super().__init__(token=code1, client_id=code2, nick=code3, prefix='!', initial_channels=[code4])
        self.command_target = None
        self.wstate = None
        self.wcity = None
        self.weatherformat = None
        self.weather = None
        self.weatherlimit = 25
        self.tempresult = False

        self.ideasdb = "AddOn_Functionality/User_DB/Ideas.db"

        self.twitchapi_headers = {'Client-ID': f"{code2}", 'Authorization': f"Bearer {Dmatru_token}"}

        self.response = requests.get(f"https://api.twitch.tv/helix/users?login={code4[1:]}",
                                     headers=self.twitchapi_headers)
        if self.response.status_code == 200:
            data = self.response.json()['data']
            if data:
                self.owner_twitch_id = data[0]
                self.owner_name = self.owner_twitch_id['display_name']
                self.owner_twitch_id = self.owner_twitch_id['id']
                print(f"Completed: ID : {self.owner_twitch_id}, Name: {self.owner_name}")

        for file in sorted(os.listdir("cogs")):
            if file.endswith("cog.py"):
                self.load_module("cogs." + file[:-3])
                print(f"{file} loaded.")

    print("Connecting...")

    async def event_ready(self):
        print(f'Ready boss, {self.nick} is connected to channel(s): {code4} ')
        print(f'Checking for tables')
        weather_db.WeatherStuff().tbl_check()
        print(f'Check completed.')
        print("-----------------")

    async def event_message(self, ctx):
        self.tempresult= False
        self.triggercheck = False

## erroring line for some reason - only when commands are used, though it provides a valid response
        print("authorname: ", ctx.author.name)
        self.response = requests.get(f"https://api.twitch.tv/helix/users?login={ctx.author.name}",
                                     headers=self.twitchapi_headers)
        print("self check")
        print(self.response)

        if self.response.status_code == 200:
            data = self.response.json()['data']
            if data:
                self.requester = data[0]
                self.requester_id = self.requester['id']
                # self.requester_id = "135764218"
                self.requester_name = self.requester['display_name']
                print(f"Name: {self.requester_name}, ID: {self.requester_id}, Message: {ctx.content}")
            else:
                pass
        else:
           pass

        # DNS is a trigger for if statements when the message for the response needs to stop going through.
        DNS = False

        ## Read chat messages Later to be used in a UI for a scene on OBS or similar.

        if str.startswith(str(ctx.content), PREFIX):
            self.command_target = ctx.content

            print(f"I saw a message with this command in line: {ctx.content}")
            print(str(ctx.content[1:]))
            if ' ' in ctx.content:
                self.commandname = ctx.content[1:].split()[0]
                non_author_target = ctx.content[1:].split()[1]
                print("Split: " + non_author_target)
            else:
                self.commandname = ctx.content[1:]


            #Checks to see if a comannd does exist currently from the bot with the cogs, set trigger to true.
            ########## To Do: modify the current set up so it compares if value is in a list vs looping through it
            ########## This way we don't need a trigger check if statements, just one or the other.
            for command in self.commands:
                print(f"Command:{command} being compared to {self.commandname}")
                if self.commandname == command:
                    self.triggercheck = True

            # If by chance the command has been found, run it.
            if self.triggercheck:
                await Mjolnirbot.handle_commands(self, message=ctx)
                self.triggercheck = False
            else:

            # If it isn't, then check the DB of custom commands

                self.dbtest = "Twitch/CMD_DB/Twitch_Commands.db"
                db = sqlite3.connect(self.dbtest)
                cur = db.cursor()
                cur.execute("SELECT DISTINCT CommandContents, CommandAction FROM Twitch_CommandList WHERE CommandName = '" +
                            str(self.commandname) + "'")
                result = (cur.fetchall())

                ########## Modify the table to include a counter for the commmand to see how many attempts to be used.
                ########## This will allow owner to identify if they should really make a command.
                if not result:
                    print(result)
                    print("Failed to find command, checking the ideas list, and if not - adding to the list.")
                    print(f"Idea ---- {str(ctx.content)}")
                    idea_to_add = str(ctx.content[1:])
                    Ideas_DB.tablestuff.checkfirst(self, user=self.requester_name, msg_dtl=idea_to_add)
                    await ctx.channel.send(
                        "Well, no command exists for that yet! No worries - I sent this command as an idea to Daz!")

                else:

                    # This will check to identify if any changes should be made to the messages before sending.

                    for row in result:
                        conditional_reply = row[1]
                        print("CR = " + conditional_reply)
                        print("User: ", row[0])
                        self.theresult = row[0]
                        print(self.theresult)

                        match conditional_reply:
                            case "AuthorOnly":
                                self.theresult = self.theresult.replace("{target}", ctx.author.name)

                            case "TargetOnly":
                                try:
                                    self.theresult = self.theresult.replace("{target}", non_author_target)
                                except UnboundLocalError:
                                    await ctx.channel.send("Well now, hold up, we need a target for this command. Don't forget to @ somebody!")
                                    DNS = True

                            case "TargetandValue":
                                self.theresult = self.theresult.replace("{target}", ctx.author.name)
                                self.theresult = self.theresult.replace("{value}", str(random.randint(1, 100)))

                        if not DNS:
                            await ctx.channel.send(self.theresult)
                        else:
                            DNS = False

mj = Mjolnirbot()

if __name__ == "__main__":
    # Background_Threads.scheduler_job().plan_job()
    mj.run()
