import discord
import json
import datetime
import os
import pytz
import time
import asyncio
from discord.ext import commands

class CommandsinLine(commands.Cog):

    def __init__(self, client):
        self.client = client

    # EchoTest
    @commands.command(pass_context=True)
    async def echo(self, ctx):
        print(f"""{ctx.message.content}""")
        msgstr = ctx.message.content[9:]
        await ctx.channel.send(f"{msgstr}")

        # Clear Channel
    @commands.command(pass_context=True)
    async def rmvmsg(self, ctx, userName: discord.User, num=1000):
        counter = 0
        await ctx.message.delete()
        msg = []
        async for msg in ctx.channel.history(limit=num):
            if msg.author.id == userName.id:
                counter += 1
                await msg.delete()
        botmsg = await ctx.message.channel.send(
            f"""Process completed. Removed {counter} messages by {userName} in this channel. This message will be deleted in three seconds.""")
        await asyncio.sleep(3)
        await botmsg.delete()


def setup(client):
    client.add_cog(CommandsinLine(client))