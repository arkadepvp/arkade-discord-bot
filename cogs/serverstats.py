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
        arkade = self.client.get_guild(439900471025467403)
        arkadeusers = self.client.get_channel(532997531022655508)
        serverpop = self.client.get_channel(536661782543073280)
        logchannel = self.client.get_channel(502380398261567490)
        statchannel = self.client.get_channel(541029645739491349)
        statMessage = await statchannel.get_message(541041088367165450)
        viprole = arkade.get_role(496896677983158272)
        reprole = arkade.get_role(441322834451759104)
        pvprole = arkade.get_role(527829610134765568)
        pverole = arkade.get_role(527945578613571604)
        while True:
            pvpServers = ['https://api.battlemetrics.com/servers/2563723', 'https://api.battlemetrics.com/servers/2563863', 'https://api.battlemetrics.com/servers/2563815', 'https://api.battlemetrics.com/servers/2563816', 'https://api.battlemetrics.com/servers/2563814', 'https://api.battlemetrics.com/servers/2822178']
            pveServers = ['https://api.battlemetrics.com/servers/3012917', 'https://api.battlemetrics.com/servers/3012916', 'https://api.battlemetrics.com/servers/3012789', 'https://api.battlemetrics.com/servers/3096726', 'https://api.battlemetrics.com/servers/3013095', 'https://api.battlemetrics.com/servers/3176233']
            pvpPlayers = 0
            pvePlayers = 0
            for server in pvpServers:
                r = requests.get(server, params=None)
                res = r.json()
                pvpPlayers = pvpPlayers + res['data']['attributes']['players']
            for server in pveServers:
                r = requests.get(server, params=None)
                res = r.json()
                pvePlayers = pvePlayers + res['data']['attributes']['players']

            totalusers = "Users: {}".format(len(arkade.members))
            vipusers = "VIPs: {}".format(len(viprole.members))
            repusers = "Reps: {}".format(len(reprole.members))
            servercount = "Players: {}".format(pvpPlayers + pvePlayers)

            await arkadeusers.edit(name=totalusers)
            await serverpop.edit(name=servercount)

            dt = datetime.datetime.now() - timedelta(hours=5)
            dt.strftime("%m-%d %H:%M:%S")

            await asyncio.sleep(5)

            embed = discord.Embed(title="Population Stats", description="Last update: " + str(dt.strftime("%m-%d %H:%M:%S")) + " EST\n", color=0xFF00FF)
            embed.add_field(name="Users", value="{}".format(len(arkade.members)), inline="true")
            embed.add_field(name="VIPs", value="{}".format(len(viprole.members)), inline="true")
            embed.add_field(name="Reps", value="{}".format(len(reprole.members)), inline="true")
            embed.add_field(name="PvP Role", value="{}".format(len(pvprole.members)), inline="true")
            embed.add_field(name="PvE Role", value="{}".format(len(pverole.members)), inline="true")
            embed.add_field(name="\u200b", value="\u200b", inline="true")
            embed.add_field(name="\u200b\nPvP Servers" + "\u2003"*25 + "_ _", value="Total: {}".format(pvpPlayers))
            for server in pvpServers:
                r = requests.get(server, params=None)
                res = r.json()
                res['data']['attributes']['players']
                playerC = res['data']['attributes']['players']
                serverN = res['data']['attributes']['name']
                serverN = (serverN[11:]).split(' ', 1)[0]
                embed.add_field(name=serverN, value="{}".format(playerC), inline="true")

            embed.add_field(name="\u200b\nPvE Servers" + "\u2003"*25 + "_ _", value="Total: {}".format(pvePlayers))
            for server in pveServers:
                r = requests.get(server, params=None)
                res = r.json()
                res['data']['attributes']['players']
                playerC = res['data']['attributes']['players']
                serverN = res['data']['attributes']['name']
                serverN = (serverN[11:]).split(' ', 1)[0]
                embed.add_field(name=serverN, value="{}".format(playerC), inline="true")

            message = await statMessage.edit(embed=embed)
            await logchannel.send("**Success.** Time: `" + str(dt.strftime("%Y-%m-%d %H:%M:%S")) + " EST`")

            await asyncio.sleep(290)

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
        embed = discord.Embed(title="Population Stats", description="\n\u200b\n", color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)

    # killbot command
    @commands.command()
    async def kill(self, ctx):
        self.client.close()


def setup(client):
    client.add_cog(serverstats(client))
