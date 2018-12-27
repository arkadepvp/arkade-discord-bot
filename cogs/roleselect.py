import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class roleselect:
    def __init__(self, client):
        self.client = client

    #join command
    @commands.command()
    async def join(self, ctx, string):
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name="TestRole")
        user = ctx.message.author
        await user.add_roles(role)

    #leave command
    @commands.command()
    async def leave(self, ctx, string):
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name="TestRole")
        user = ctx.message.author
        await user.remove_roles(role)

def setup(client):
    client.add_cog(roleselect(client))
