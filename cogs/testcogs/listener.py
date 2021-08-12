import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        help = 'help'
        tag = 'tag'
        word = help
        if word.lower() in message.content.lower():
            await message.channel.send(f'Your message contained the word "{word}". To access the help bot please type -help')

def setup(client):
    client.add_cog(help(client))
