import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import app_commands
import json
import datetime
import pytz
import asyncio

def read_token():
    with open("../Config/Secret", "r") as f:
        lines = f.readlines()
        return lines[6].strip()
token = read_token()

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


########    ########    ########    Slash commands    ########    ########    ########    ########
class mjdbot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1052226107371421816))
        self.synced = True
        print("Yo, I be online yo")

client = mjdbot()
tree = app_commands.CommandTree(client)

#
@tree.command(name="ping", description="Pings you.", guild=discord.Object(id=1052226107371421816))
async def ping(interation: discord.Interaction):
    await interation.response.send_message(f"You have been pinged.")

    ########    ########    ########    Slash Commands End   ########    ########    ########

    ########    ########    ########    Listener only - if on, no commands run   ########    ########    ########

# # @client.event
# # async def on_message(message):
# #     if message.content == "hello".lower():
# #         await message.channel.send("Yo!")

    ########    ########    ########    End above - if on, no commands run   ########    ########    ########

    ########    ########    ########    Server Events   ########    ########    ########


# @client.event
# async def on_member_join(member):
#     channel = member.guild.system_channel
#     await channel.send(f"{member.mention}, Welcome to Daz's most glorious Server!")


    ########    ########    ########    Server Events END  ########    ########    ########

    ########    ########    ########    Commands Only  ########    ########    ########

# @client.command()
# async def halllp(ctx):
#     await ctx.reply(f"Oh the commands are coming soon. For now, I'm jusssst watching. ;)")

# @client.command()
# async def embed(ctx, member: discord.Member = None):
#     if member == None:
#         member = ctx.author
#
#     mem_name = member.display_name
#     pfp = member.display_avatar
#
#     embed = discord.Embed(title="Title", description="A Description", color=discord.Color.random())
#     embed.set_author(name=f"{mem_name}", url="www.google.com", icon_url="https://static.vecteezy.com/system/resources/thumbnails/006/899/230/small/mystery-random-loot-box-from-game-icon-vector.jpg")
#     embed.set_thumbnail(url=f"{pfp}")
#     embed.add_field(name="FieldOne", value="This a value")
#     embed.add_field(name="inline field", inline=True)
#     embed.add_field(name="NOT field", inline=False)
#     embed.set_footer(text=f"{mem_name} made this")
#
#     await ctx.send(embed=embed)

    ########    ########    ########   Commands only END   ########    ########    ########

print('Connecting...')

# @client.event
# async def on_ready():
#    print("Aw yeah I'm reconnected")
# await bot.change_presence(status=discord.Status.dnd, activity.discord.Game("Bringing the hammer down!")


#Run bot
client.run(token)
