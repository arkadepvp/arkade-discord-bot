import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class ticketsort:
    def __init__(self, client):
        self.client = client

    #ticketsort
    
def setup(client):
    client.add_cog(ticketsort(client))
