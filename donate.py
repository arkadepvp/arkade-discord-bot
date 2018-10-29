import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from lxml import html
import requests
import sys

class donate:
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(donate(client))
