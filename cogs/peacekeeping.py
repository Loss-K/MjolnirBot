import discord
import json
import time
import asyncio
from discord.ext import commands
from discord.ext.commands import Cog

with open('Jsons/Blocked_Words.json') as f:
    config = json.load(f)

class PeaceKeeperCog(Cog):

    def __init__(self, bot):
        self.bot = bot

        # Sets up Cusscounter by author -
        self.cussCounter = {}

        self.spm_dm_warn = """Automated Warning: It looks like you've said the same thing three times. This is 
        considered spam. If you continue, you will be muted for 24 hours. """

        self.blocked_dm_warn = """Automated Warning: Please remember the #positivevibesonly guideline when speaking in 
        our server. If you continue, you will be muted for 24 hours."""

        self.both_dm_warn = """Automated Warning: Please remember the #positivevibesonly and spamming guidelines when 
        speaking in our server. If you continue, you will be muted for 24 hours."""


        self.blk_three_times = False
        self.blk_five_times = False

    @Cog.listener("on_message")
    async def chk_msg(self, message):

        if not message.author.bot and not message.content.startswith("!"):
            print(f"I saw a message: {message.content}")
            await self.blk_checker(message)
            await self.spm_checker(message)
            # await self.modding(message)
            await self.msg_decisions(message)
            await self.blkwrd_time_check(message)

    async def blk_checker(self, message):

        #looks to see if they exist in the list already.
        if message.author.id not in self.cussCounter:
            print("The cusser wasn't in the list - adding")
            print(message.author.id)
            print(self.cussCounter)
            self.cussCounter[message.author.id] = {'lastknownusername_discriminator': message.author.name + "#" +
                                                    message.author.discriminator,
                                                   'cussCount': 0,
                                                   'lastCuss': time.time()}

        if any([str.lower(word) in str.lower(message.content) for word in config['words']]):
            # If the user isn't already logged, create an initial object with a count of 0 to avoid errors.
            if time.time() - self.cussCounter[message.author.id]["lastCuss"] > 86400:
                self.cussCounter[message.author.id]["cussCount"] = 0

            # Now take action to tally the cuss count and mark the time it happened
            self.cussCounter[message.author.id]["cussCount"] += 1
            self.cussCounter[message.author.id]["lastCuss"] = time.time()

            print("Found a bad word" + " by the author " + str(message.author) + "'. Count is now " + str(
                self.cussCounter[message.author.id]["cussCount"]) + ".")

    async def spm_checker(self, message):
        self.spam_counter = 0
        self.spm_three_times = False
        self.spm_five_times = False

        async for msg in message.channel.history(limit=50):
            if msg.author.id == message.author.id and str.lower(message.content) == str.lower(
                    msg.content) and message.author != message.author.bot:
                self.spam_counter = self.spam_counter + 1

        print("Spmcount: " + str(self.spam_counter))

    async def blkwrd_time_check(self, message):
        if any([str.lower(word) in str.lower(message.content) for word in config['words']]):
            self.cussbool = True
            await self.modding(message)
        else:
            self.cussbool = False
            print("No")

    async def modding(self, message):

        # doghouse_role = discord.utils.get(discord.Client.guild.roles, name='Doghouse')

        #  and self.cussCounter[message.author.id]['lastCuss'] > 3:

        if self.cussCounter[message.author.id]["cussCount"] >= 1 and self.cussbool:
            # print(f"Wondering if: {self.cussCounter[message.author.id]['lastCuss'] -300 }")
            print("Warning in Chat sent.")
            botmsg = await message.channel.send('{}: {}'.format(message.author.mention, config['response']))
            await message.delete()
            await asyncio.sleep(6)
            await botmsg.delete()

    async def msg_decisions(self, message):
        match self.cussCounter[message.author.id]["cussCount"]:
            case _ if 5 > self.cussCounter[message.author.id]["cussCount"] >= 3:
                blkthreetimes = True
                await message.author.send(self.blocked_dm_warn)
                print("User said a bad word three times.")

            case _ if self.cussCounter[message.author.id]["cussCount"] >= 5:
                print("User said a bad word 5+ times.")

        match self.spam_counter:
            case _ if 4 > self.spam_counter >= 3:
                await message.author.send(self.spm_dm_warn)
            case _ if self.spam_counter >= 5:
                spmfivetimes = True

async def setup(bot):
    await bot.add_cog(PeaceKeeperCog(bot))
