from twitchio.ext import commands
import Ideas_DB


class ideascogger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='idea')
    async def idea_addition(self, ctx, *, user = None):
        self.command_target = self.bot.command_target
        idea_to_add = str(self.command_target[6:])
        print("---Audit to add--")
        print(idea_to_add)
        Ideas_DB.tablestuff().checkfirst(user=ctx.author.name, msg_dtl=idea_to_add)
        await ctx.send(f"What a grand idea! I've added it onto my back end list for vetting!")


def prepare(bot: commands.Bot):
    bot.add_cog(ideascogger(bot))
    print("cog added")
