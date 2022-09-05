from twitchio.ext import commands

with open("../Config/Secret", "r") as f:
    lines = f.readlines()
    code1 = str.lower(lines[0]).strip()
    code2 = str.lower(lines[1]).strip()
    code3 = str.lower(lines[2]).strip()
    code4 = str.lower(lines[3]).strip()

PREFIX = "!"


class Mjolnirbot(commands.Bot):

    def __init__(self):
        super().__init__(token=code1, client_id=code2, nick=code3, prefix='!', initial_channels=[code4])

    print("Connecting...")

    async def event_ready(self):
        print(f'Ready boss, {self.nick} is connected to channel(s): {code4} ')

###Prevent conversation with itself ######

    async def event_message(self, ctx):
        if str.startswith(str(ctx.content), PREFIX):
            print("I saw a message with this command in line")

        # if ctx.author.name.lower() == str.lower(code3):
        #     print("I saw my own message.")
        #     return

        await self.handle_commands(ctx)

    ############## Dang it dude you're so close.
    # Read up on https://twitchio.readthedocs.io/en/latest/twitchio.commands.html#errors

    #
    # if commands.core.check(ctx):
    # await self.handle_commands(ctx)
    # else:
    #     print("yikes")

    # if CommandNotFound:
    #     # pass
    #     print('Test failed.')
    #     # return

    # if await self.event_command_error(ctx,error=CommandNotFound):
    #     print("Oh No")

############################Command List ############################

    #### If No Commands Exist Then tell them that ####

    ##Event Commands##

    # Lurk like a Pro

    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send(f"Commands are:")
        await ctx.send(f"lurk")
        await ctx.send(f"unlurk")
        await ctx.send(f"SC - Not finished")
        await ctx.send(f"thorsday")
        await ctx.send(f"pom")
        await ctx.send(f"assemble")



    @commands.command(name='unlurk')
    async def unlurk(self, ctx):
        await ctx.send(f"A flash of light cuts through the clouds in the sky and hits the ground."
                       f" As the light dissipates, @{ctx.author.name} steps forward, victorious from their conquest.")

    @commands.command(name='lurk')
    async def lurk(self, ctx):
        await ctx.send(f"@{ctx.author.name} calls forth the bifrost, disappearing in a bright light to complete "
                       f"a glorious quest of their own.")

    ############################ Information ############################

    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('Test completed.')

    # CurrentSong

    @commands.command(name='sc')
    async def sc(self, ctx):
        await ctx.send('Currently Playing... Who knows (coming soon.)')

    #Thorsday

    @commands.command(name='thorsday')
    async def thorsday(self, ctx):
        await ctx.send(f"Thorsday is Daz's favorite day! He will rock it, scream it, and crush it. Join the fray..."
                       f"(Rewrite this)")

    #Pomodoros

    @commands.command(name='pom')
    async def pom(self, ctx):
        await ctx.send(f"During pomodoros ( https://en.wikipedia.org/wiki/Pomodoro_Technique ), "
                       "Daz may be engaged in battle with a mighty task, and sometimes that means more focus. "
                       "This would be a great time for you to catch up on some work, side projects, whatever you want. "
                       "We'll all take a break together and chill together once you hear the battle roar.")

    ##Social Media Stuffs

    @commands.command(name='socials')
    async def social(self, ctx):
        await ctx.send('Socials:')

    # Assemble
    @commands.command(name='assemble')
    async def assemble(self, ctx):
        await ctx.send('TITANS!!!! MAKE YE KNOWN! ASSEEEMMMMMBLLLEEEE')


mj = Mjolnirbot()

if __name__ == "__main__":
    mj.run()