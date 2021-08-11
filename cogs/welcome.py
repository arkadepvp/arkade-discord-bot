import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        await channel.send(f"{member} has arrived!")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        word = 'hello'
        if word.lower() in message.content.lower():
            await message.channel.send(f'Hello! Welcome {message.author.name}!')



def setup(client):
    client.add_cog(welcome(client))
