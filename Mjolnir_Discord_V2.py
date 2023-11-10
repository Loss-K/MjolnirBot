import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import app_commands
import os
import json
import datetime
import pytz
import asyncio


def read_token():
    with open("./Config/Secret", "r") as f:
        lines = f.readlines()
        return lines[6].strip()

token = read_token()


class MjolnirDC(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

        self.start_time = datetime.datetime.utcnow()
        print(f"Turned on: {self.start_time}")

        asyncio.run(self.load())

    async def load(self):

        initial_cogs = [
            'cogs.peacekeeping',
            'cogs.commands_list',
            'cogs.StandardBotCommands'
        ]

        for ext in initial_cogs:
            try:
                await self.load_extension(ext)
                print(f"loaded cog: {ext}")
            except Exception as error:
                print(f"Failed to load extension {ext!r}: {error}")


# Run bot
print('Connecting...')

if __name__ == "__main__":
    MjolnirDC().run(token)
