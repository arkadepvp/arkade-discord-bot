import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot


class CommandErrorHandler:
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(CommandErrorHandler(client))
