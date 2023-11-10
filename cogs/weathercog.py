from twitchio.ext import commands
import requests
import datetime
import weather_db


with open("./Config/Secret", "r") as f:
    lines = f.readlines()
    wcode = str(lines[5]).strip()

class testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.confirm = True
        self.weatherlimit = 25

    @commands.command(name='weather')
    async def weathercheck(self, ctx, *, user = None):
        print("I got here.")
        self.command_target = self.bot.command_target
        self.command_target = self.command_target[9:]
        self.user = self.bot.requester['display_name']

        self.weather = self.command_target.replace(",", "%2C%20")
        self.wcity = str(self.command_target.split(',')[0]).strip()
        self.wstate = str(self.command_target.split(',')[1]).strip()
        print(self.wcity)
        print(self.wstate)

        if self.weatherlimit == 0:
            await ctx.send(
                f"Unfortunately the limit has been reached today. I'm using a freebie plan at this time. "
                f"Try again tomorrow!")
        else:
            if str(self.command_target).find(',') == -1:
                await ctx.send("Incorrect format. Try in City,ST format. ie !weather Tampa,FL")

            else:
                ## First Check the DB if it exists

                self.key_check = weather_db.WeatherStuff().pull_key(wcity=self.wcity, wstate=self.wstate)

                # If it doesn't return a key then call for it
                if self.key_check is None:
                    loc_key_search_url = 'http://dataservice.accuweather.com/locations/v1/cities/search?q='
                    city_name = self.weather

                    comb_url = loc_key_search_url + city_name + "&apikey=" + wcode + "&details=false"
                    loc_key_response = requests.get(comb_url)
                    loc_key_json = loc_key_response.json()
                    city_key = loc_key_json[0].get('Key')

                    weather_db.WeatherStuff().confirmstate(city=self.wcity, statereq=self.wstate, loc_key=city_key)

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

def prepare(bot: commands.Bot):
    bot.add_cog(testing(bot))
    print("cog added")
