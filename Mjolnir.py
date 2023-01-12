import string
import time
from twitchio.ext import commands
import msg_log_db
import Ideas_DB
import random
import datetime
import requests

import json
import requests

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

    print("Connecting...")

    async def event_ready(self):
        print(f'Ready boss, {self.nick} is connected to channel(s): {code4} ')
        print(f'Checking for tables')
        msg_log_db.tablestuff().tbl_check()
        weather_db.WeatherStuff().tbl_check()
        Ideas_DB.tablestuff().tbl_check()
        print(f'Check completed.')

    ## If No Commands Exist Then tell them that ####
    ## Logging does not work.

    async def event_command_error(self, ctx, error: Exception) -> None:
        cauth = ctx.author.name
        errstr = str(error)
        errupdated = errstr.translate(str.maketrans('', '', string.punctuation))
        cmdname = str(error)[12:-12]
        testdb = msg_log_db
        testdb.tablestuff().cmd_update(user=cauth, cmd_dtl=errupdated, cmd_name=cmdname)

        if errupdated == "No command " + cmdname + " was found":
            await ctx.send(f"Hey @{cauth}, This command doesn't exist! "
                           f"Don't worry, I sent the idea to Daz directly. :)")
        else:
            await ctx.send(f"Hey @dazinmatru, we had an error when {cauth} tried to run the command! "
                           f"If it exists, check the script: {error}")

    async def event_message(self, ctx):
        authorcheck = ctx.author

        if authorcheck is not None and not str.startswith(str(ctx.content), PREFIX):
            # Bot_Logging

            msg_log_db.tablestuff().tbl_update(user=ctx.author.name, msg_dtl=ctx.content)

            # Found a command from the user

        if str.startswith(str(ctx.content), PREFIX):
            print("I saw a message with this command in line")

            ## We need the ID of the requester
            self.response = requests.get(f"https://api.twitch.tv/helix/users?login={ctx.author.name}",
                                         headers=self.twitchapi_headers)
            if self.response.status_code == 200:
                data = self.response.json()['data']
                if data:
                    self.requester = data[0]
                    self.requester_id = self.requester['id']
                    # self.requester_id = "135764218"
                    self.requester_name = self.requester['display_name']
                    print(f"Name: {self.requester_name}, ID: {self.requester_id}")
                else:
                    pass
            else:
                pass

            self.command_target = ctx.content.split(" ", 1)
            if len(self.command_target) > 1:
                self.command_target = self.command_target[1]
                print(f"{self.command_target} was the result")
            else:
                print("0 found, proceed with code")
                self.command_target = None

            await self.handle_commands(ctx)

    # ###########################Command List ############################

    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send(f"Commands in stream can be found here: https://dazinmatru.com/#twitchcommands")

    @commands.command(name="followage")
    async def followage(self, ctx):
        # print(f"{broadcaster_name} has id {broadcaster_id}")
        self.response = requests.get(
            f"https://api.twitch.tv/helix/users/follows?from_id={self.requester_id}&to_id={self.owner_twitch_id}",
            headers=self.twitchapi_headers)
        self.result = self.response.json()
        self.result = self.result['data']

        # followed_day = self.result[0]['followed_at'][8:10]
        # followed_month = self.result[0]['followed_at'][5:7]
        # followed_year = self.result[0]['followed_at'][:4]
        followed_total = datetime.datetime(int(self.result[0]['followed_at'][:4]), int(self.result[0]['followed_at'][5:7]), int(self.result[0]['followed_at'][8:10]), 12, 0, 0)
        totaltime = datetime.datetime.now() - followed_total
        totaltime = str(totaltime).split(',', 1)
        await ctx.send(f"Dang @{self.result[0]['from_name']}!"
                       f" You've been following me for a total of {totaltime[0]}! "
                       f"Since {self.result[0]['followed_at'][5:7]}/{self.result[0]['followed_at'][:4]}!")

    @commands.command(name='clip')
    async def clip_things(self, ctx):
        self.response = requests.post(f"https://api.twitch.tv/helix/clips?broadcaster_id={self.owner_twitch_id}",
                                 headers= self.twitchapi_headers)
        self.result = self.response.json()
        self.result = self.result['data']

        print(self.result[0]['id'])
        clipURL = "https://clips.twitch.tv/" + self.result[0]['id']
        await ctx.send(f"You've been caught @Dazinmatru! {ctx.author.name} has clipped you in action. "
                       f"Everybody can watch it here: {clipURL}")

        print(self.result)

    @commands.command(name='unlurk')
    async def unlurk(self, ctx):
        await ctx.send(f"A flash of light cuts through the clouds in the sky and hits the ground."
                       f" As the light dissipates, @{ctx.author.name} steps forward, victorious from their conquest."
                       f" What a classic Thor adventure!")

    @commands.command(name='lurk')
    async def lurk(self, ctx):
        await ctx.send(f"@{ctx.author.name} calls forth the bifrost, disappearing in a bright light to complete "
                       f"a glorious quest of their own.")

    # ########################### Information ############################

    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('Test completed.')

    # CurrentSong

    @commands.command(name='sc')
    async def sc(self, ctx):
        await ctx.send(f'Currently Playing form the Lofi Girl Channel on Youtube: '
                       f'https://www.youtube.com/watch?v=jfKfPfyJRdk')

    # Thorsday

    @commands.command(name='thorsday')
    async def thorsday(self, ctx):
        await ctx.send(f"Thorsday is Daz's favorite day! He will rock it, scream it, and crush it. Join the fray..."
                       f"(Rewrite this)")

    # Pomodoros

    @commands.command(name='pom')
    async def pom(self, ctx):
        await ctx.send(f"During pomodoros ( https://en.wikipedia.org/wiki/Pomodoro_Technique ), "
                       "Daz may be engaged in battle with a mighty task, and sometimes that means more focus. "
                       "This would be a great time for you to catch up on some work, side projects, whatever you want. "
                       "We'll all take a break together and chill together once you hear the battle roar.")

    # # Social Media Stuffs

    @commands.command(name='socials')
    async def social(self, ctx):
        await ctx.send('Check me out on https://www.dazinmatru.com! (Everything is new, so it is still in progress)')

    # Assemble
    @commands.command(name='tassemble')
    async def assemble(self, ctx):
        await ctx.send('TITANS!!!! MAKE YE KNOWN! ASSEEEMMMMMBLLLEEEE')

    @commands.command(name='down')
    async def down(self, ctx):
        rannum = random.randint(1, 100)
        await ctx.send(f"@{ctx.author.name} jumps high into the sky, lightning raging around them."
                       f" reaching the peak of the jump, they smirk, eyes glowing as they "
                       f"look down at their target... They rush to the ground slamming and"
                       f" bringing the hammer down with {str(rannum)}% focus!")

    # ### Epic people ####

    @commands.command(name='pink')
    async def pink(self, ctx):

        if ctx.author.name.lower() == "pinkfairysaku" or ctx.author.name.lower() == "dazinmatru":
            target = msg_log_db.tablestuff().pick_random()
            await ctx.send(f"@{ctx.author.name} grabs her bow, tugging back the arrow. She closes her eyes, letting go."
                           f" The arrow shoots out with a beam of light following"
                           f" and hits {target} with her love arrow! FEEL THE LOVE!")
        else:
            await ctx.send(f"@{ctx.author.name}, only the great pinkfairysaku can use this command!")

    @commands.command(name='sylver')
    async def sylver(self, ctx):
        if ctx.author.name.lower() == "sylverdreamer" or ctx.author.name.lower() == "dazinmatru":

            await ctx.send(f"The world of Twitch begins to shake. Mountains move, and the gentle waters of the seas"
                           f" become large waves. Gusts of wind circle like a powerful twister... And the dirt on"
                           f" the ground find its way off thousands of pieces... of glorious Legos, and"
                           f" they rise from the depths of the earth... and in a lego built seat sits"
                           f" @{ctx.author.name} smiling proudly, ready to shake this channel up with his army of lego "
                           f" built Marvel heroes...")

            await ctx.send(f"@{ctx.author.name} has phenomenal building streams and comic readings! Go give"
                           f" this epic dude a follow! www.twitch.tv/sylverdreamer")
        else:
            await ctx.send(f"@{ctx.author.name}, only the great Sylverdreamer can use this command!")

    @commands.command(name='daz')
    async def daz(self, ctx):
        await ctx.send(f"Howdy, I'm Kev, also known as Daz. Welcome to the party! I love all things Thor related. "
                       f"THORSDAY (Thursdays) is my favorite day of the week! "
                       f"I call my self a technology counselor as my job title. My normal day consists of individuals "
                       f"coming to me with their technical issues, and I dive in to find the solution "
                       f"and provide advice. I'm currently working to level up as a developer. ")

    @commands.command(name='bye')
    async def bye(self, ctx):
        await ctx.send(f"Thank you for tuning in! You can check me out on dazinmatru.com. This is"
                       f" my site that will contain my social medias, merch, and all the good stuff!")

    @commands.command(name='so')
    async def shoutout(self, ctx):
        if self.command_target is None:
            await ctx.send(f"No target found.")
        else:
            await ctx.send(f"Hold up! You don't know the great {self.command_target}? "
                           f"You should check out their channel"
                           f" and give them a follow! www.twitch.tv/{self.command_target.replace('@', '')}!")

    @commands.command(name='stream')
    async def streaminfo(self, ctx):
        await ctx.send(f"My streams will consist of either chill co-working sessions, "
                       f"gaming to what I can on my Laptop."
                       f"I'm still working out a new schedule, so keep an eye on the schedule tab "
                       f"Anybody is welcome to chill and have another classic Thor Adventure!"
                       f"Wanna see what I'm up to for the stream? Check out my Figma plan: "
                       f"https://www.figma.com/file/UDwdo4n3mhVQH1mLBcXZQi/Untitled?node-id=0%3A1&t=Y9UnyKRRfTK8ftLS-1")

    @commands.command(name='raid')
    async def raid(self, ctx):
        await ctx.send(f"BOP BOP BOP We are here to BRING THE HAMMER DOWN! BOP BOP BOP")

    @commands.command(name='hug')
    async def hug(self, ctx):
        if self.command_target is None:
            await ctx.send(f"No target found.")
        else:
            await ctx.send(f"@{ctx.author.name} runs up to {self.command_target} and gives them the biggest, "
                           f"most crushing hug ever!")

    @commands.command(name='gn')
    async def gn(self, ctx):
        if self.command_target is None:
            await ctx.send(f"No target found. You need to specify who you want to tuck into bed!")
        else:
            await ctx.send(f"@{ctx.author.name} catches {self.command_target} yawning. Using their mighty muscles, "
                           f"they pick up and {self.command_target} into their room, screaming "
                           f"'GOOD NIGHT', walking away proudly at their victory.")

    @commands.command(name='idea')
    async def idea_addition(self, ctx):
        idea_to_add = str(self.command_target)
        Ideas_DB.tablestuff().tbl_update(user=ctx.author.name, msg_dtl=idea_to_add)
        await ctx.send(f"What a grand idea! I've added it onto my back end list for vetting!")


    # Weather Stuff to be moved in its own Addon Functionality

    @commands.command(name='weather')
    async def weathercheck(self, ctx):

        self.weather = self.command_target.replace(",", "%2C%20")
        self.wcity = str(self.command_target.split(',')[0]).strip()
        self.wstate = str(self.command_target.split(',')[1]).strip()
        print(self.wcity)
        print(self.wstate)

        if self.weatherlimit == 0:
            await ctx.send(f"Unfortunately the limit has been reached today. I'm using a freebie plan at this time. "
                           f"Try again tomorrow!")
        else:
            if str(self.command_target).find(',') == -1:
                await ctx.send("Incorrect format. Try in City,ST format. ie !weather Tampa,FL")

            else:
                ## First Check the DB if it exists

                self.key_check = weather_db.WeatherStuff().pull_key(wcity=self.wcity, wstate=self.wstate)

                #If it doesn't return a key then call for it
                if self.key_check is None:
                    loc_key_search_url = 'http://dataservice.accuweather.com/locations/v1/cities/search?q='
                    city_name = self.weather

                    comb_url = loc_key_search_url + city_name + "&apikey=" + wcode + "&details=false"
                    loc_key_response = requests.get(comb_url)
                    loc_key_json = loc_key_response.json()

                    city_key = loc_key_json[0].get('Key')

                    weather_db.WeatherStuff().tbl_update(city=self.wcity, state=self.wstate, loc_key=city_key)

                    self.weatherlimit = self.weatherlimit - 1

                else:
                    city_key = self.key_check
                    print("Ok, Found the key and used it instead of using a second call.")

                ## Now that we have a key, we can request actual details about that location.

                city_search_url = 'http://dataservice.accuweather.com/currentconditions/v1/'
                comb_url = city_search_url + city_key + "?apikey=" + wcode + "&details=True"

                city_weather_response = requests.get(comb_url)

                actual_weather_json = city_weather_response.json()

                weather_dtl = actual_weather_json[0]

                weather_type = weather_dtl["WeatherText"]
                metric = weather_dtl["Temperature"]["Metric"]["Value"]
                imperial = weather_dtl["Temperature"]["Imperial"]["Value"]
                realfeel_m = weather_dtl["RealFeelTemperature"]["Metric"]["Value"]
                realfeel_i = weather_dtl["RealFeelTemperature"]["Imperial"]["Value"]

                self.weatherlimit = self.weatherlimit - 1

                print(f"{self.weatherlimit} weather calls remaining")

                await ctx.send(f"The weather in {self.wcity}, {self.wstate} is {weather_type}, at a temperature "
                               f"of {imperial}F/{metric}C. It feels like it's really {realfeel_i}F/{realfeel_m}C")

    ### Admin Commands ###

    @commands.command(name='clr_db')
    async def cleardb(self, ctx):
        confirm = ctx.author.name
        if confirm == "dazinmatru":
            print("Prepping table for destruction")
            msg_log_db.tablestuff().tbl_cleanup()
            print("Table Crushed.")
            await ctx.send(f"Completed.")

    @commands.command(name='es_strim')
    async def endstream(self, ctx):
        confirm = ctx.author.name
        if confirm == "dazinmatru":
            await ctx.send(f"done!")
            await mj.close()
            time.sleep(15)
            await Mjolnirbot.close(self)
            exit()
        else:
            await ctx.send(f"You do not have the power to do this.")


mj = Mjolnirbot()

if __name__ == "__main__":
    mj.run()
