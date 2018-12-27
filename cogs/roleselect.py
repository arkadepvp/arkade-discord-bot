import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class roleselect:
    def __init__(self, client):
        self.client = client

    #join command
    @commands.command()
    async def join(self, ctx):
        await ctx.message.delete()

        await client.add_roles(ctx.message.author, discord.utils.get(user.server.roles, name="TestRole"))

    #leave command
    @commands.command()
    async def leave(self, ctx):
        await ctx.message.delete()


def setup(client):
    client.add_cog(roleselect(client))
