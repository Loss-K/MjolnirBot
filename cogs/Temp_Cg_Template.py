from twitchio.ext import commands

class COGGERNAME(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='COMMANDNAME')
    async def COMMANDFUNCTION(self, ctx, *, user = None):
        pass


def prepare(bot: commands.Bot):
    bot.add_cog(COGGERNAME(bot))
    print("cog added")
