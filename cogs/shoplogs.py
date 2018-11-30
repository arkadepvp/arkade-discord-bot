import discord
import asyncio
import urllib.request
import time
import json
from discord.ext import commands
from discord.ext.commands import Bot
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

with open('configfinal.json', 'r') as f:
    config = json.load(f)

class shopcharts:
    def __init__(self, client):
        self.client = client

    #shopchart command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def shopchart(self, ctx):
        await ctx.message.delete()
        #COLLECT DATA

        #Sets user and pass vars.
        ftp1 = config['ftp1user'] + ':' + config['ftp1pass']
        ftp2 = config['ftp2user'] + ':' + config['ftp2pass']
        ftp3 = config['ftp3user'] + ':' + config['ftp3pass']

        #download from ArkadePvP server
        urllib.request.urlretrieve('ftp://' + ftp1 + '@147.135.8.214/Servers/S3C1M1-L1P-Ragnarok/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Ragnarok.log', 'shoplogs/ShopLog_Ragnarok.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://' + ftp2 + '@147.135.9.6/Servers/S3C1M2-L2P-Aberration/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Aberration_P.log', 'shoplogs/ShopLog_Aberration.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://' + ftp1 + '@147.135.8.214/Servers/S3C1M1-L2P-Center/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_TheCenter.log', 'shoplogs/ShopLog_TheCenter.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://' + ftp1 + '@147.135.8.214/Servers/S3C1M1-L3P-Island/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_TheIsland.log', 'shoplogs/ShopLog_TheIsland.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://' + ftp2 + '@147.135.9.6/Servers/S3C1M2-L3P-Scorched/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_ScorchedEarth_P.log', 'shoplogs/ShopLog_ScorchedEarth.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://' + ftp3 + '@147.135.8.210/Servers/S3C1M3-L1P-Extinction2/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Extinction.log', 'shoplogs/ShopLog_Ext2.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://' + ftp2 + '@147.135.9.6/Servers/S3C1M2-L1P-Extinction/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Extinction.log', 'shoplogs/ShopLog_Ext1.log')

        filenames = ['shoplogs/ShopLog_Ragnarok.log', 'shoplogs/ShopLog_Aberration.log', 'shoplogs/ShopLog_TheCenter.log', 'shoplogs/ShopLog_TheIsland.log', 'shoplogs/ShopLog_ScorchedEarth.log', 'shoplogs/ShopLog_Ext1.log', 'shoplogs/ShopLog_Ext2.log']
        with open('shoplogs/Combined_Log.log', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())

        with open('shoplogs/Combined_Log.log', 'r') as f:
            combined = f.readlines()

        buysellOnly=[]
        for s in combined:
            if s.find('bought item') != -1:
                buysellOnly.append(s)

        finalList = [((x.split('\"', 1)[-1]).replace('\". Amount - ', ',')).rstrip('\n') for x in buysellOnly]

        finalItemOnly = [(x.split(',')[0]) for x in finalList]
        uniqueList = []
        for x in finalItemOnly:
            if x not in uniqueList:
                uniqueList.append(x)
        uniqueList.sort()

        itemlist = finalItemOnly
        numberlist = [(x.split(',', 1)[-1]) for x in finalList]

        counter = 0
        uniqueCounter = [0] * len(uniqueList)

        for x in uniqueList:
            smallCounter = 0
            for y in itemlist:
                if x == y:
                    uniqueCounter[counter] += int(numberlist[smallCounter])
                smallCounter += 1
            counter += 1

        printList = []
        fmt = '{:<12}{}'
        for i, (item, quantity) in enumerate(zip(uniqueList, uniqueCounter)):
            printList.append(fmt.format(item, quantity))
        try:
            printListOne = printList[0:50]
            printListTwo = printList[50:100]
            printListThree = printList[100:150]
        except Exception as e:
            print(e)

        printStringOne = "\n".join(str(e) for e in printListOne)
        printStringTwo = "\n".join(str(e) for e in printListTwo)
        printStringThree = "\n".join(str(e) for e in printListThree)

        # PLOT CREATION

        objects = uniqueList[0:100]
        performance = uniqueCounter[0:100]
        y_pos = np.arange(len(objects))

        plt.figure(figsize=(40,20))
        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects, rotation='vertical')
        plt.ylabel('Number Bought')
        plt.title('Items Purchaced In Store')

        plt.savefig('shoplogs/shopchart.png', bbox_inches='tight')
        # END PLOT CREATION

        #SEND EMBED TO DISCORD
        embed = discord.Embed(title="Items Purchaced Chart", description="```Item        #     || Item        #```", color=0xCC33CC)
        embed.add_field(name="1-50", value="```" + printStringOne + "```")
        embed.add_field(name="51-100", value="```" + printStringTwo + "```")
        message = await ctx.message.channel.send(embed=embed)

        await ctx.message.channel.send("All time shop chart", file=discord.File('shoplogs/shopchart.png'))

def setup(client):
    client.add_cog(shopcharts(client))