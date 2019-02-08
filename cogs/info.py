import discord
import asyncio
import json
import time
from discord.ext import commands
from discord.ext.commands import Bot

startTime = time.time()

with open('help.json', 'r') as f:
    help = json.load(f)


class info:
    def __init__(self, client):
        self.client = client

    # help command
    @commands.command(aliases=['commands'])
    async def help(self, ctx, string=None):
        embed = discord.Embed(title="**Help: **", description="**Command arguments are shown with <> and are required.**", color=0x589BFF)
        permLevel = 0
        if 472999533635436545 in [y.id for y in ctx.author.roles]:
            permLevel = 1
        if 441322476991938571 in [y.id for y in ctx.author.roles]:
            permLevel = 1

        for category in help:
            categoryFormat = category.capitalize()
            embed.add_field(name=f"\u200b\n**{categoryFormat}**", value="_ _", inline=False)
            for command in help[category]:
                if int(command['level']) <= permLevel:
                    cmd = command['cmd']
                    usage = command['usage']
                    desc = command['desc']
                    embed.add_field(name=f"`.{usage}` - {desc}", value="_ _", inline=False)

        message = await ctx.message.channel.send(embed=embed)

    # info command
    @commands.command(aliases=['information'])
    async def info(self, ctx):
        await ctx.message.delete()

        secs = (time.time() - startTime)
        days = secs//86400
        hours = (secs - days * 86400)//3600
        minutes = int(secs - days * 86400 - hours * 3600)//60
        seconds = int(secs - days * 86400 - hours * 3600 - minutes * 60)

        days = int(days)
        hours = int(hours)
        minutes = int(minutes)

        embed = discord.Embed(title="_ _", description="A custom built bot for the [Arkade PvP Discord.](https://discord.gg/G8d5YFd)", color=0x589BFF)
        embed.set_author(name="Arkade PvP | Bot Stats")
        embed.set_thumbnail(url="https://s3-us-west-2.amazonaws.com/www.guilded.gg/user_content/image/de968c2d-8f58-4778-f007-720acab23e3e.png")
        embed.add_field(name="Members", value="{}".format(len(ctx.guild.members)), inline=True)
        embed.add_field(name="Uptime", value="{}d {}h {}m {}s".format(days, hours, minutes, seconds), inline=True)
        embed.add_field(name="Links", value="• [GitHub | arkade-discord-bot](https://github.com/arkadepvp/arkade-discord-bot)]\n• [GitHub | arkade-website](https://github.com/arkadepvp/arkade-website)\n")
        embed.set_footer(text="Made by N0XIRE#0001 | Python 3.6.6 & Discord.py rewrite", icon_url="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/49/49f52da179dfbc200d532ac09c550a9be09e1371_full.jpg")
        message = await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(info(client))
