import discord
import asyncio
import json
import math
from discord.ext import commands
from discord.ext.commands import Bot

with open('configfinal.json', 'r') as f:
    config = json.load(f)


class admin:
    def __init__(self, client):
        self.client = client

    # poll command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def poll(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="📊 | Vote ✅ or ❌ on the question below.\n_ _", description=" ".join(string), color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

    # sqrt command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def sqrt(self, ctx, time: float):
        addedTime = round((2*(math.sqrt(time))), 1)
        totalTime = addedTime + time
        message = await ctx.message.channel.send(f"The increase in ban time should be: {addedTime} The new total ban time should be: {totalTime}")

    # servers command
    @commands.command(aliases=['server'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def servers(self, ctx, *string):
        await ctx.message.delete()
        pvpServers = ""
        pveServers = ""
        eventServers = ""

        for server in config['arkPvpServers']:
            pvpServers = pvpServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"

        for server in config['arkPveServers']:
            pveServers = pveServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"

        for server in config['arkEventServers']:
            eventServers = eventServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"

        embed = discord.Embed(title="Server Direct Connect Links", description="-", color=0xFF00FF)
        embed.add_field(name="PVP Server Links", value=pvpServers)
        embed.add_field(name="PVE Server Links", value=pveServers)
        embed.add_field(name="Event Server Links", value=eventServers)
        message = await ctx.message.channel.send(embed=embed)

    # multipoll command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def multipoll(self, ctx, *string):
        await ctx.message.delete()

        pollList = list(string)
        multiList = ['?', '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭']

        try:
            pollList[1] = "🇦 " + pollList[1]
            pollList[2] = "🇧 " + pollList[2]
            pollList[3] = "🇨 " + pollList[3]
            pollList[4] = "🇩 " + pollList[4]
            pollList[5] = "🇪 " + pollList[5]
            pollList[6] = "🇫 " + pollList[6]
            pollList[7] = "🇬 " + pollList[7]
            pollList[8] = "🇭 " + pollList[8]
        except:
            pass
        embed = discord.Embed(title="📊 | Vote on the question below.\n", description="".join(pollList[0]), color=0xFF00FF)
        embed.add_field(name="---", value="\n".join(pollList[1:]))

        message = await ctx.message.channel.send(embed=embed)

        for i in range(1, len(pollList)):
            await message.add_reaction(multiList[i])

    # welcome command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def welcome(self, ctx):
        await ctx.message.delete()
        links = ""
        for link in config['links']:
            links = links + "✦ " + "[" + link['Title'] + "](" + link['URL'] + ")\n"

        embed = discord.Embed(title="Welcome to Arkade!", description="**A PvP and PvE ARK community.**\n\u200b\n", color=0xFF00FF)
        embed.add_field(name="Rates", value="✦ EXP: 3x\n✦ Gathering: 5x\n✦ Taming: 7x\n✦ Breeding: 10x (15x PvE)\n✦ Character Level: 105 +30\n✦ Wild Dino Level: 150\n\u200b\n", inline="true")
        embed.add_field(name="Links", value=links, inline=True)
        embed.add_field(name="Quick Information", value="✦ Please read <#556891543391174657> or <#525499381789491201> for our rules/config.\n✦ Check <#472558681687457792> for our connect and vote links.\n✦ Ping *@Arkade Admin* in <#472623301290622993> if there is a server crash.\n\u200b\n")
        embed.add_field(name="Self Assignable Roles", value="Add your reaction to any of the available role options that you want to join.\nSelecting a role will give you access to the relevant discussion channels in this Discord server.  You may choose more than one role.\n\n**ARK PvP: **:bow_and_arrow:\n**ARK PvE: **:hammer:\n**ARK 6Man: **:six:")
        welcomeMsg = await ctx.channel.get_message(527842025329131521)
        message = await welcomeMsg.edit(embed=embed)

    # links command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def links(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(title="Trello", description=config['trello'], color=0xFF00FF)
        embed.add_field(name="Information", value=config['information'], inline=False)
        embed.add_field(name="Community Links", value=config['community'], inline=False)
        linkMsg = await ctx.channel.get_message(568297134969847809)
        message = await linkMsg.edit(embed=embed)

def setup(client):
    client.add_cog(admin(client))
