import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class donate:
    def __init__(self, client):
        self.client = client

    async def on_ready():
        pass

def setup(client):
    client.add_cog(donate(client))
