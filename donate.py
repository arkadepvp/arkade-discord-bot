import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class donate:
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        channel = client.get_channel('502380383434833920')
        message = await self.client.send_message(channel, "test")

def setup(client):
    client.add_cog(donate(client))
