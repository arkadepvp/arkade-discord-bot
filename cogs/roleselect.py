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

        string = string.lower()

        if string == "pvp":
            role = discord.utils.get(ctx.guild.roles, name="PvP")
        elif string == "pve":
            role = discord.utils.get(ctx.guild.roles, name="PvE")
        else:
            message = await ctx.message.channel.send("Error: Improper Role", delete_after=5)

        user = ctx.message.author

        try:
            await user.add_roles(role)
            message = await ctx.message.channel.send("Success!", delete_after=5)
        except:
            message = await ctx.message.channel.send("Error: Improper Role", delete_after=5)

    #leave command
    @commands.command()
    async def leave(self, ctx, string):
        await ctx.message.delete()

        string = string.lower()

        if string == "pvp":
            role = discord.utils.get(ctx.guild.roles, name="PvP")
        elif string == "pve":
            role = discord.utils.get(ctx.guild.roles, name="PvE")
        else:
            message = await ctx.message.channel.send("Error: Improper Role", delete_after=5)

        user = ctx.message.author

        try:
            await user.remove_roles(role)
            message = await ctx.message.channel.send("Success!", delete_after=5)
        except:
            message = await ctx.message.channel.send("Error: Improper Role", delete_after=5)

def setup(client):
    client.add_cog(roleselect(client))
