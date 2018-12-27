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

        if string.lower() == "pvp":
            role = discord.utils.get(ctx.guild.roles, name="PvP")
        else:
            pass
        if sting.lower() == "pve":
            role = discord.utils.get(ctx.guild.roles, name="PvE")
        else:
            pass

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

        if string.lower() == "pvp":
            role = discord.utils.get(ctx.guild.roles, name="PvP")
        else:
            pass
        if sting.lower() == "pve":
            role = discord.utils.get(ctx.guild.roles, name="PvE")
        else:
            pass

        user = ctx.message.author

        try:
            await user.remove_roles(role)
            message = await ctx.message.channel.send("Success!", delete_after=5)
        except:
            message = await ctx.message.channel.send("Error: Improper Role", delete_after=5)

def setup(client):
    client.add_cog(roleselect(client))
