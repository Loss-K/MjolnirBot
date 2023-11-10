from twitchio.ext import commands
import requests
import datetime
import weather_db

class Twitchcog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("./Config/Secret", "r") as f:
            lines = f.readlines()
            code1 = str.lower(lines[0]).strip()
            code2 = str.lower(lines[1]).strip()
            code3 = str.lower(lines[2]).strip()
            code4 = str.lower(lines[3]).strip()
            self.wcode = str(lines[5]).strip()
            Dmatru_token = str(lines[8]).strip()


    # @commands.command(name="followage")
    # async def followage(self, ctx):
    #     print("I got here")
    #
    #     # print(f"{broadcaster_name} has id {broadcaster_id}")
    #     self.response = requests.get(
    #         f"https://api.twitch.tv/helix/users/follows?from_id={self.bot.requester_id}&to_id={self.bot.owner_twitch_id}",
    #         headers=self.bot.twitchapi_headers)
    #     self.result = self.response.json()
    #     #self.result = self.result['data']
    #     print(self.result)
    #
    #     followed_total = datetime.datetime(int(self.result[0]['followed_at'][:4]), int(self.result[0]['followed_at'][5:7]),
    #                                        int(self.result[0]['followed_at'][8:10]), 12, 0, 0)
    #     totaltime = datetime.datetime.now() - followed_total
    #     totaltime = str(totaltime).split(',', 1)
    #     await ctx.send(f"Dang @{self.result[0]['from_name']}!"
    #                    f" You've been following me for a total of {totaltime[0]}! "
    #                    f"Since {self.result[0]['followed_at'][5:7]}/{self.result[0]['followed_at'][:4]}!")


    @commands.command(name='clip')
    async def clip_things(self, ctx):
        print("I got here")
        self.response = requests.post(f"https://api.twitch.tv/helix/clips?broadcaster_id={self.bot.owner_twitch_id}",
                                      headers=self.bot.twitchapi_headers)
        self.result = self.response.json()
        self.result = self.result['data']

        print(self.result[0]['id'])
        clipURL = "https://clips.twitch.tv/" + self.result[0]['id']
        await ctx.send(f"You've been caught @{self.bot.owner_name}! {ctx.author.name} has clipped you in action. "
                       f"Everybody can watch it here: {clipURL}")

        print(self.result)

def prepare(bot: commands.Bot):
    bot.add_cog(Twitchcog(bot))
    print("cog added")
