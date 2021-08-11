import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class tag(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tag(self, ctx, *text):
        str = ' '
        str = str.join(text)
        await ctx.send(str)
        file = open("/home/programming/arkadeBot/tags.txt", "a")
        file.write(str)
        file.close()
        file = open("/home/programming/arkadeBot/tags.txt", "r")
        contents = file.read()
        await ctx.send(contents)
        file.close()

def setup(client):
    client.add_cog(tag(client))
