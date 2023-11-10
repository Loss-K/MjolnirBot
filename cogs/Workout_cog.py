from twitchio.ext import commands
import json
import random
class COGGERNAME(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='workout', aliases="wo")
    async def workoutfunction(self, ctx, *, user = None, top_amount=None, random_tick=True):
        confirm = self.bot.requester['display_name']
        print(ctx.author.name)
        if confirm.lower() == "dazinmatru":
            with open("Jsons/Exercises.json", "r") as file:
                stat = json.load(file)

            original_values = list(stat)

            self.random_exercise = random.choice(original_values)

            # Check for errors first
            if not isinstance(top_amount, int) and top_amount is not None:
                error_rmks = "The value is Not Int"
                await ctx.send(error_rmks)

            # If user wants to do the same amount every time.
            if top_amount is not None and not random_tick:
                self.topamount = int(top_amount)
            # if user wants a totally random number up to 25
            elif top_amount is None and random_tick:
                self.random_amount = random.choice(range(10, 25))
            # if user wants a totally random number with a limit entered
            elif top_amount is not None and random_tick:
                self.topamount = int(top_amount)
                self.random_amount = random.choice(range(10, self.topamount))
            else:
                error_rmks = "Something went wrong."
                await ctx.send(error_rmks)

            if str(self.random_exercise[2]).lower() == "time":
                self.random_amount = "30 second"

            await ctx.send(f"You need to do {self.random_amount} {self.random_exercise[0]}. "
                           f"If you haven't done a {self.random_exercise[0]} before, here is a video: "
                           f"{self.random_exercise[1]}")


def prepare(bot: commands.Bot):
    bot.add_cog(COGGERNAME(bot))
    print("cog added")
