import discord
import asyncio
import json
import datetime
from datetime import timedelta
import requests
from discord.ext import commands
from discord.ext.commands import Bot

with open('counter.json', 'r') as f:
    count = json.load(f)


class serverstats:
    def __init__(self, client):
        self.client = client
        self.bg_task = self.client.loop.create_task(self.getstats())

    async def on_member_join(self, member):
        join = int(count['join'])
        join = join + 1
        count['join'] = str(join)
        with open('counter.json', 'w') as f:
            json.dump(count, f)

    async def on_member_remove(self, member):
        leave = int(count['leave'])
        leave = leave + 1
        count['leave'] = str(leave)
        with open('counter.json', 'w') as f:
            json.dump(count, f)

    async def getstats(self):
        await asyncio.sleep(3)
        arkade = self.client.get_guild(439900471025467403)
        arkadeusers = self.client.get_channel(532997531022655508)
        serverpop = self.client.get_channel(536661782543073280)
        logchannel = self.client.get_channel(502380398261567490)
        statchannel = self.client.get_channel(541029645739491349)
        statMessage = await statchannel.get_message(541478737716314122)
        statMessagePvP = await statchannel.get_message(541478744955682818)
        statMessagePvE = await statchannel.get_message(541478812613869579)
        viprole = arkade.get_role(496896677983158272)
        reprole = arkade.get_role(441322834451759104)
        pvprole = arkade.get_role(527829610134765568)
        pverole = arkade.get_role(527945578613571604)

        pvpServers = {'2563723', '2563815', '2563814', '2822178', '2563816', '2563863'}
        pveServers = {'3012917', '3012916', '3096726', '3013095', '3012789', '3183242', '3176233', '3328636', '3362284', '3346652', '3394143'}
        miscServers = {'2792094', '3222091', '3382712'}

        pvpTotal = 0
        pveTotal = 0
        miscTotal = 0

        while True:
            # BEGIN PVP STATS
            embedPvP = discord.Embed(title="PVP Population Stats", description=f"Total: {pvpTotal}", color=0x58A9FA)
            embedPvP.add_field(name="\u200b\nPvP Servers" + "\u2003"*25 + "_ _", value="Total: {}".format(pvpTotal))

            for serverID in pvpServers:

                r = requests.get('https://api.battlemetrics.com/servers/' + serverID, params=None)
                serverPop = r.json()['data']['attributes']['players']

                pvpTotal = pvpTotal + serverPop

                embedPvP.add_field(name="Ragnarok", value="{}".format(pvpRag), inline="true")

            messagePvP = await statMessagePvP.edit(embed=embedPvP)
            # END PVP STATS

            # BEGIN PVE STATS
            embedPvE = discord.Embed(title="PVP Population Stats", description=f"Total: {pvpTotal}", color=0x58A9FA)
            embedPvE.add_field(name="\u200b\nPvP Servers" + "\u2003"*25 + "_ _", value="Total: {}".format(pvpTotal))

            for serverID in pveServers:

                r = requests.get('https://api.battlemetrics.com/servers/' + serverID, params=None)
                serverPop = r.json()['data']['attributes']['players']

                pveTotal = pveTotal + serverPop

                embedPvE.add_field(name="Ragnarok", value="{}".format(pvpRag), inline="true")

            messagePvP = await statMessagePvP.edit(embed=embedPvE)
            # END PVE STATS

            totalusers = "Users: {}".format(len(arkade.members))
            vipusers = "VIPs: {}".format(len(viprole.members))
            repusers = "Reps: {}".format(len(reprole.members))
            servercount = "Players: {}".format(pvpTotal + pveTotal + miscTotal)

            await arkadeusers.edit(name=totalusers)
            await serverpop.edit(name=servercount)

            joinCnt = int(count['join'])
            leaveCnt = int(count['leave'])
            jlRatio = round((float(joinCnt)/float(leaveCnt))*100, 2)

            dt = datetime.datetime.now() - timedelta(hours=5)
            dt.strftime("%m-%d %H:%M:%S")

            pvpCount = 0
            pveCount = 0
            for member in viprole.members:
                if pvprole in member.roles:
                    pvpCount = pvpCount + 1
                elif pverole in member.roles:
                    pveCount = pveCount + 1

            embed = discord.Embed(title="Discord Population Stats", description=f"Last update: " + str(dt.strftime("%m-%d %H:%M")) + " EST\n", color=0xFF00FF)
            embed.add_field(name="Users", value="{}".format(len(arkade.members)), inline="true")
            embed.add_field(name="PvP Role", value="{}".format(len(pvprole.members)), inline="true")
            embed.add_field(name="PvE Role", value="{}".format(len(pverole.members)), inline="true")
            embed.add_field(name="VIPs", value="{}".format(len(viprole.members)), inline="true")
            embed.add_field(name="PvP VIPs", value="{}".format(pvpCount), inline="true")
            embed.add_field(name="PvE VIPs", value="{}".format(pveCount), inline="true")
            embed.add_field(name="Reps", value="{}".format(len(reprole.members)), inline="true")
            embed.add_field(name="Join/Leave Raw", value=f"{joinCnt}/{leaveCnt}", inline="true")
            embed.add_field(name="Join/Leave Ratio", value=f"{jlRatio}%", inline="true")

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
