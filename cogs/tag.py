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
        file = open("/home/programming/arkadeBot/cogs/generated.py", "w")
        file.write('''\
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class generated(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        word = 'help'
        if word.lower() in message.content.lower():
            await message.channel.send(f'Your message contained the word "{word}". To access the help bot please type -help')

def setup(client):
    client.add_cog(generated(client))
    ''')
        file.close()
        file = open("/home/programming/arkadeBot/cogs/generated.py", "r")
        contents = file.read()
        await ctx.send(contents)
        file.close()

def setup(client):
    client.add_cog(tag(client))
