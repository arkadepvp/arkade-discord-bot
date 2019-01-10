import discord
import asyncio
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
            await asyncio.sleep(15)

    #killtask command
    @commands.command()
    async def killtask(self, ctx):
        self.bg_task.cancel()
        await ctx.message.channel.send("Task ended")

    #starttask command
    @commands.command()
    async def starttask(self, ctx):
        self.bg_task = self.client.loop.create_task(self.getstats())
        await ctx.message.channel.send("Task started")

def setup(client):
    client.add_cog(serverstats(client))
