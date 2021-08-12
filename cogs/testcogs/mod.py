import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mod(self, ctx):
        await ctx.send('mod')

    #could take in the id of a spammer that another bot will detect by monitoring the chat and then passing through their author.id
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)

    @commands.command()
    async def ban(self, ctx):
            await ctx.send('ban command')

def setup(client):
    client.add_cog(mod(client))
