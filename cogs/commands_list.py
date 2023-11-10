import discord
import json
import time
import asyncio
from discord.ext import commands
from discord.ext.commands import Cog
from discord import app_commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class CommList(Cog):
    def __init__(self, client):
        self.client = client

        # To remove the precreated helpscreen for now.
        client.remove_command("help")

    @commands.command()
    async def ping(self, message):
        await message.channel.send(f"Yo {message.author.name}")

    @commands.command()
    async def help(self, message):
        await message.channel.send(f"You can find all the commands here: <https://dazinmatru.com/#discordcommands>")

    @commands.command()
    async def rmvmsg(self, message, userName: discord.User, num=1000):
        counter = 0
        await message.message.delete()
        msg = []
        async for msg in message.channel.history(limit=num):
            if msg.author.id == userName.id:
                counter += 1
                await msg.delete()
        botmsg = await message.channel.send(
            f"""Process completed. Removed {counter} messages by {userName} in this channel. This message will be deleted in three seconds.""")
        await asyncio.sleep(3)
        await botmsg.delete()


async def setup(bot):
    await bot.add_cog(CommList(bot))
