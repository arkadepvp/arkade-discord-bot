import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class donate:
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        message = await self.client.send_message(502380383434833920, "test")

def setup(client):
    client.add_cog(donate(client))
