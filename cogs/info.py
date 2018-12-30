import discord
import asyncio
import time
from discord.ext import commands
from discord.ext.commands import Bot

startTime = time.time()

class info:
    def __init__(self, client):
        self.client = client

    #oldhelp command
    @commands.command()
    async def oldhelp(self, ctx, string=None):

        embed = discord.Embed(title="Help: ", description="Command arguments are shown with <> and are required.\n", color=0x50bdfe)
        embed.add_field(name="General Commands", value="`.help` -  Displays this information\n`.info` - Displays info about the bot")
        embed.add_field(name="Ark Commands", value="`.craft <item>` -  Display crafting requirments for an item\n`.search <query>` -  Searches [gamepedia](https://ark.gamepedia.com) for the given query\n`.map <map>` -  Displays a picture of the given map.\n`.tame <creature>` -  In development.\n`.wiki <creature>` -  Displays basic wiki info of the given dinosaur")
        if string == "admin":
            embed.add_field(name="Admin Commands", value="`.poll <question>` - Creates a poll with the given question\n`.multipoll <\"question\" \"answer1\">` - Creates a poll with the given question and up to eight answers.\n`.welcome` - Sends the welcome message in the active channel\n`.play <url>` - Plays a youtube link (must be in a voice channel)\n`.fire` - A nice relaxing fireplace (must be in a voice channel)\n`.stop` - Stops whatever is currently playing")
        message = await ctx.message.channel.send(embed=embed)

    #info command
    @commands.command(name="info", brief="Displays info about the bot")
    async def info(self, ctx):
        await ctx.message.delete()

        secs = (time.time() - startTime)
        days = secs//86400
        hours =  (secs - days * 86400)//3600
        minutes  = int(secs - days * 86400 - hours * 3600)//60
        seconds = int(secs - days * 86400 - hours * 3600 - minutes * 60)

        days = int(days)
        hours = int(hours)
        minutes = int(minutes)

        embed = discord.Embed(title="_ _", description="A custom built bot for the [Arkade PvP Discord.](https://discord.gg/G8d5YFd)", color=0x50bdfe)
        embed.set_author(name="Arkade PvP | Bot Stats", icon_url="https://s3-us-west-2.amazonaws.com/www.guilded.gg/user_content/image/de968c2d-8f58-4778-f007-720acab23e3e.png")
        embed.set_thumbnail(url="https://s3-us-west-2.amazonaws.com/www.guilded.gg/user_content/image/de968c2d-8f58-4778-f007-720acab23e3e.png")
        embed.add_field(name="Members", value="{}".format(len(ctx.guild.members)), inline=True)
        embed.add_field(name="Uptime", value="{}d {}h {}m {}s".format(days, hours, minutes, seconds), inline=True)
        embed.add_field(name="Links", value="T\nB\nD")
        embed.set_footer(text="Made in Python 3.6.6 with Discord.py rewrite | Made by N0XIRE#7589", icon_url="https://s3-us-west-2.amazonaws.com/www.guilded.gg/user_content/image/de968c2d-8f58-4778-f007-720acab23e3e.png")
        message = await ctx.message.channel.send(embed=embed)

def setup(client):
    client.add_cog(info(client))
