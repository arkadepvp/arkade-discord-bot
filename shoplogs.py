import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class shoplogs:
    def __init__(self, client):
        self.client = client

    #poll command
    @commands.command(pass_context=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def poll(self, ctx, *string):
        embed = discord.Embed(title="", description="", color=0xCC33CC)
        await self.client.send_message(pollChannel, embed=embed)

def setup(client):
    client.add_cog(shoplogs(client))
