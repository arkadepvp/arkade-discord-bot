import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class serverstats:
    def __init__(self, client):
        self.client = client

    async def getstats(self):
        while not client.is_closed:
            channel = client.get_channel(502380348932358145)
            new_name = "test"
            await channel.edit(name=new_name)
            await asyncio.sleep(5)

    client.loop.create_task(serverstats())

def setup(client):
    client.add_cog(serverstats(client))
