import discord
import asyncio
import datetime
from discord.ext import commands
from discord.ext.commands import Bot

class serverstats:
    def __init__(self, client):
        self.client = client

    async def getstats(self):
        arkade = self.client.get_guild(439900471025467403)
        arkadedev = self.client.get_guild(492879703250698251)
        arkadeusers = self.client.get_channel(532997531022655508)
        arkadevips = self.client.get_channel(533011684479205376)
        arkadereps = self.client.get_channel(533011717551030273)
        logchannel = self.client.get_channel(502380398261567490)
        viprole = arkade.get_role(496896677983158272)
        reprole = arkade.get_role(441322834451759104)
        test = self.client.get_channel(502380383434833920)
        while True:
            totalusers =  "Users: {}".format(len(arkade.members))
            vipusers =  "VIPs: {}".format(len(viprole.members))
            repusers =  "Reps: {}".format(len(reprole.members))
            await arkadeusers.edit(name=totalusers)
            await arkadevips.edit(name=vipusers)
            await arkadereps.edit(name=repusers)
            dt = datetime.datetime.now()
            dt.strftime("%Y-%m-%d %H:%M:%S")
            await logchannel.send("**Success.** Time: `" + str(dt.strftime("%Y-%m-%d %H:%M:%S")) + "`")
            await asyncio.sleep(300)

    #killtask command
    @commands.command()
    async def killtask(self, ctx):
        try:
            self.bg_task.cancel()
            await ctx.message.channel.send("Task ended.")
        except:
            await ctx.message.channel.send("Task wasn't running.")

    #starttask command
    @commands.command()
    async def starttask(self, ctx):
        try:
            self.bg_task = self.client.loop.create_task(self.getstats())
            await ctx.message.channel.send("Task started.")
        except:
            await ctx.message.channel.send("Task failed to start.")

    #killbot command
    @commands.command()
    async def kill(self, ctx):
        self.client.close()


def setup(client):
    client.add_cog(serverstats(client))
