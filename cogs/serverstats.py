import discord
import asyncio
import datetime
from datetime import timedelta
import requests
from discord.ext import commands
from discord.ext.commands import Bot


class serverstats:
    def __init__(self, client):
        self.client = client
        self.bg_task = self.client.loop.create_task(self.getstats())

    async def getstats(self):
        await asyncio.sleep(3)
        arkade = self.client.get_guild(439900471025467403)
        arkadeusers = self.client.get_channel(532997531022655508)
        serverpop = self.client.get_channel(536661782543073280)
        logchannel = self.client.get_channel(502380398261567490)
        statchannel = self.client.get_channel(541029645739491349)
        statMessage = await statchannel.get_message(541478737716314122)
        statMessageTwo = await statchannel.get_message(541478744955682818)
        statMessageThree = await statchannel.get_message(541478812613869579)
        viprole = arkade.get_role(496896677983158272)
        reprole = arkade.get_role(441322834451759104)
        pvprole = arkade.get_role(527829610134765568)
        pverole = arkade.get_role(527945578613571604)
        while True:
            pvpServers = ['https://api.battlemetrics.com/servers/2563723', 'https://api.battlemetrics.com/servers/2563863', 'https://api.battlemetrics.com/servers/2563815', 'https://api.battlemetrics.com/servers/2563816', 'https://api.battlemetrics.com/servers/2563814', 'https://api.battlemetrics.com/servers/2822178']
            pveServers = ['https://api.battlemetrics.com/servers/3012917', 'https://api.battlemetrics.com/servers/3012916', 'https://api.battlemetrics.com/servers/3012789', 'https://api.battlemetrics.com/servers/3096726', 'https://api.battlemetrics.com/servers/3013095', 'https://api.battlemetrics.com/servers/3176233']

            r = requests.get('https://api.battlemetrics.com/servers/2563723', params=None)
            pvpRag = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/2563815', params=None)
            pvpAbb = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/2563814', params=None)
            pvpCen = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/2822178', params=None)
            pvpExt = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/2563816', params=None)
            pvpIsl = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/2563863', params=None)
            pvpSch = r.json()['data']['attributes']['players']

            r = requests.get('https://api.battlemetrics.com/servers/3012917', params=None)
            pveRag = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/3012916', params=None)
            pveAbb = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/3096726', params=None)
            pveCen = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/3013095', params=None)
            pveExt = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/3012789', params=None)
            pveIsl = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/3183242', params=None)
            pveSch = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/3176233', params=None)
            pveVal = r.json()['data']['attributes']['players']

            r = requests.get('https://api.battlemetrics.com/servers/2792094', params=None)
            miscEv = r.json()['data']['attributes']['players']
            r = requests.get('https://api.battlemetrics.com/servers/3222091', params=None)
            miscDM = r.json()['data']['attributes']['players']

            pvpTotal = pvpRag + pvpAbb + pvpCen + pvpExt + pvpIsl + pvpSch
            pveTotal = pveRag + pveAbb + pveCen + pveExt + pveIsl + pveSch + pveVal
            miscTotal = miscEv + miscDM

            totalusers = "Users: {}".format(len(arkade.members))
            vipusers = "VIPs: {}".format(len(viprole.members))
            repusers = "Reps: {}".format(len(reprole.members))
            servercount = "Players: {}".format(pvpTotal + pveTotal + miscTotal)

            await arkadeusers.edit(name=totalusers)
            await serverpop.edit(name=servercount)

            dt = datetime.datetime.now() - timedelta(hours=5)
            dt.strftime("%m-%d %H:%M:%S")

            pvpCount = 0
            pveCount = 0
            for member in viprole.members:
                if pvprole in member.roles:
                    pvpCount = pvpCount + 1
                elif pverole in member.roles:
                    pveCount = pveCount + 1

            embed = discord.Embed(title="Discord Population Stats", description=f"Last update: " + str(dt.strftime("%m-%d %H:%M:%S")) + " EST\n", color=0xFF00FF)
            embed.add_field(name="Users", value="{}".format(len(arkade.members)), inline="true")
            embed.add_field(name="PvP Role", value="{}".format(len(pvprole.members)), inline="true")
            embed.add_field(name="PvE Role", value="{}".format(len(pverole.members)), inline="true")
            embed.add_field(name="VIPs", value="{}".format(len(viprole.members)), inline="true")
            embed.add_field(name="PvP VIPs", value="{}".format(pvpCount), inline="true")
            embed.add_field(name="PvE VIPs", value="{}".format(pveCount), inline="true")
            embed.add_field(name="Reps", value="{}".format(len(reprole.members)), inline="true")

            embedTwo = discord.Embed(title="Server Population Stats", description=f"Total: {pvpTotal + pveTotal + miscTotal}", color=0x58A9FA)
            embedTwo.add_field(name="\u200b\nPvP Servers" + "\u2003"*25 + "_ _", value="Total: {}".format(pvpTotal))
            embedTwo.add_field(name="Ragnarok", value="{}".format(pvpRag), inline="true")
            embedTwo.add_field(name="Aberration", value="{}".format(pvpAbb), inline="true")
            embedTwo.add_field(name="The Center", value="{}".format(pvpCen), inline="true")
            embedTwo.add_field(name="Extinction", value="{}".format(pvpExt), inline="true")
            embedTwo.add_field(name="The Island", value="{}".format(pvpIsl), inline="true")
            embedTwo.add_field(name="Scorched Earth", value="{}".format(pvpSch), inline="true")

            embedTwo.add_field(name="\u200b\nPvE Servers" + "\u2003"*25 + "_ _", value="Total: {}".format(pveTotal))
            embedTwo.add_field(name="Ragnarok", value="{}".format(pveRag), inline="true")
            embedTwo.add_field(name="Aberration", value="{}".format(pveAbb), inline="true")
            embedTwo.add_field(name="The Center", value="{}".format(pveCen), inline="true")
            embedTwo.add_field(name="Extinction", value="{}".format(pveExt), inline="true")
            embedTwo.add_field(name="The Island", value="{}".format(pveIsl), inline="true")
            embedTwo.add_field(name="Scorched Earth", value="{}".format(pveSch), inline="true")
            embedTwo.add_field(name="Valguero", value="{}".format(pveVal), inline="true")

            embedTwo.add_field(name="\u200b\nMisc Servers" + "\u2003"*25 + "_ _", value="Total: {}".format(miscTotal))
            embedTwo.add_field(name="Events", value="{}".format(miscEv), inline="true")
            embedTwo.add_field(name="Deathmatch", value="{}".format(miscDM), inline="true")

            embedThree = discord.Embed(title="TBD", description="_ _", color=0xFF00FF)

            message = await statMessage.edit(embed=embed)
            messageTwo = await statMessageTwo.edit(embed=embedTwo)
            messageThree = await statMessageThree.edit(embed=embedThree)
            await logchannel.send("**Success.** Time: `" + str(dt.strftime("%m-%d %H:%M:%S")) + " EST`")

            await asyncio.sleep(299)

    # killtask command
    @commands.command()
    async def killtask(self, ctx):
        try:
            self.bg_task.cancel()
            await ctx.message.channel.send("Task ended.")
        except:
            await ctx.message.channel.send("Task wasn't running.")

    # starttask command
    @commands.command()
    async def starttask(self, ctx):
        try:
            self.bg_task = self.client.loop.create_task(self.getstats())
            await ctx.message.channel.send("Task started.")
        except:
            await ctx.message.channel.send("Task failed to start.")

    # message command
    @commands.command()
    async def message(self, ctx):
        embed = discord.Embed(title="title", description="description", color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(serverstats(client))
