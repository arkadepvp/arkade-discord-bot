import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class admin:
    def __init__(self, client):
        self.client = client

    #poll command
    @commands.command(pass_context=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def poll(self, ctx, *string):
        await self.client.delete_message(ctx.message)

        pollChannel = ctx.message.channel
        await self.client.send_message(pollChannel, "\@everyone")
        embed = discord.Embed(title=" Vote ✅ or ❌ on the question below.\n_ _", description=" ".join(string), color=0xCC33CC)
        embed.set_author(name="Poll", icon_url="https://melbournechapter.net/images/question-mark-clipart-transparent.png")
        message = await self.client.send_message(pollChannel, embed=embed)
        await self.client.add_reaction(message, '✅')
        await self.client.add_reaction(message, '❌')

    #welcome command
    @commands.command(pass_context=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def welcome(self, ctx):
        await self.client.delete_message(ctx.message)
        welcomeChannel = ctx.message.channel

        embed = discord.Embed(title="Welcome to Arkade PvP!", description="```md\nArkade PvP - More than just a server.\n-------------------------------------\n```\n", color=0xCC33CC)
        embed.set_image(url="https://cdn.discordapp.com/attachments/461022949798051871/472549308454010880/arkadebanner23.png")
        embed.add_field(name="Rates", value="✦ EXP: 3x\n✦ Gathering: 5x\n✦ Taming: 5x\n✦ Breeding: 10x\n✦ Character Level: 104 +30\n✦ Wild Dino Level: 150", inline="true")
        embed.add_field(name="Links", value="✦ [Our Website](http://arkadepvp.com)\n✦ [Guilded](https://www.guilded.gg/ArkadePvP/)\n✦ [Discord](https://discord.me/arkade)", inline="true")
        embed.add_field(name="_ _", value="_ _")
        embed.add_field(name="Quick Information", value="✦ Please read <#492888582726615040> for our rules and config settings.\n✦ Check <#472558681687457792> for our connect and vote links.\n✦ Ping @Arkade Admin in <#472623301290622993> if there is a server crash.")
        embed.add_field(name="_ _", value="_ _")
        embed.add_field(name="Server Direct Connect Links", value="✦ Ragnarok: steam://connect/147.135.8.214:27015\n✦ Aberration: steam://connect/147.135.9.6:27015\n✦ The Center: steam://connect/147.135.8.214:27017\n✦ The Island: steam://connect/147.135.8.214:27018\n✦ Scorched Earth: steam://connect/147.135.9.6:27016\n✦ Event Map: steam://connect/147.135.9.6:27051\n")
        message = await self.client.send_message(welcomeChannel, embed=embed)

def setup(client):
    client.add_cog(admin(client))
