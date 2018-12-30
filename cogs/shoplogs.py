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
    async def shopchart(self, ctx, string):
        await ctx.message.delete()
        #COLLECT DATA

        #Sets user and pass vars.
        ftp1 = config['ftp1user'] + ':' + config['ftp1pass']
        ftp2 = config['ftp2user'] + ':' + config['ftp2pass']
        ftp3 = config['ftp3user'] + ':' + config['ftp3pass']
        ftp4 = config['ftp4user'] + ':' + config['ftp4pass']
        ftp5 = config['ftp5user'] + ':' + config['ftp5pass']

        if string == "pvp":
            #download from ArkadePvP server
            urllib.request.urlretrieve('ftp://' + ftp1 + '@147.135.8.214/Servers/S3C1M1-L1P-Ragnarok/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Ragnarok.log', 'shoplogs/ShopLog_Ragnarok.log')
            time.sleep(.025)
            urllib.request.urlretrieve('ftp://' + ftp1 + '@147.135.8.214/Servers/S3C1M1-L3P-Island/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_TheIsland.log', 'shoplogs/ShopLog_TheIsland.log')
            time.sleep(.025)
            urllib.request.urlretrieve('ftp://' + ftp2 + '@147.135.9.6/Servers/S3C1M2-L2P-Aberration/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Aberration_P.log', 'shoplogs/ShopLog_Aberration.log')
            time.sleep(.025)
            urllib.request.urlretrieve('ftp://' + ftp2 + '@147.135.9.6/Servers/S3C1M2-L3P-Scorched/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_ScorchedEarth_P.log', 'shoplogs/ShopLog_ScorchedEarth.log')
            time.sleep(.025)
            urllib.request.urlretrieve('ftp://' + ftp4 + '@147.135.30.58/Servers/S3C1M4-L1P-Center/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_TheCenter.log', 'shoplogs/ShopLog_TheCenter.log')
            time.sleep(.025)
            urllib.request.urlretrieve('ftp://' + ftp3 + '@147.135.8.210/Servers/S3C1M3-L1P-Extinction2/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Extinction.log', 'shoplogs/ShopLog_Ext2.log')
            time.sleep(.025)
            urllib.request.urlretrieve('ftp://' + ftp2 + '@147.135.9.6/Servers/S3C1M2-L1P-Extinction/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Extinction.log', 'shoplogs/ShopLog_Ext1.log')

            filenames = ['shoplogs/ShopLog_Ragnarok.log', 'shoplogs/ShopLog_Aberration.log', 'shoplogs/ShopLog_TheCenter.log', 'shoplogs/ShopLog_TheIsland.log', 'shoplogs/ShopLog_ScorchedEarth.log', 'shoplogs/ShopLog_Ext1.log', 'shoplogs/ShopLog_Ext2.log']
            with open('shoplogs/Combined_Log.log', 'w') as outfile:
                for fname in filenames:
                    with open(fname) as infile:
                        outfile.write(infile.read())

        else:
            #download from ArkadePvE server
            urllib.request.urlretrieve('ftp://' + ftp5 + '@147.135.30.61/Servers/S1C2M5-L1E-Ragnarok/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Ragnarok.log', 'shoplogs/ShopLog_Ragnarok.log')
            time.sleep(.1)
            urllib.request.urlretrieve('ftp://' + ftp5 + '@147.135.30.61/Servers/S1C2M5-L2E-Island/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_TheIsland.log', 'shoplogs/ShopLog_TheIsland.log')
            time.sleep(.1)
            urllib.request.urlretrieve('ftp://' + ftp5 + '@147.135.30.61/Servers/S1C2M5-L3E-Aberration/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Aberration_P.log', 'shoplogs/ShopLog_Aberration.log')
            time.sleep(.1)
            urllib.request.urlretrieve('ftp://' + ftp5 + '@147.135.30.61/Servers/S1C2M5-L4E-Extinction/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Extinction.log', 'shoplogs/ShopLog_Ext.log')

            filenames = ['shoplogs/ShopLog_Ragnarok.log', 'shoplogs/ShopLog_Aberration.log', 'shoplogs/ShopLog_TheIsland.log', 'shoplogs/ShopLog_Ext.log']
            with open('shoplogs/Combined_Log.log', 'w') as outfile:
                for fname in filenames:
                    with open(fname) as infile:
                        outfile.write(infile.read())

        #process newly combined log
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
            printListOne = printList[1:60]
            printListTwo = printList[60:120]
            printListThree = printList[120:180]
            printListFour = printList[180:240]
        except Exception as e:
            print(e)

        printStringOne = "\n".join(str(e) for e in printListOne)
        printStringTwo = "\n".join(str(e) for e in printListTwo)
        printStringThree = "\n".join(str(e) for e in printListThree)
        printStringFour = "\n".join(str(e) for e in printListFour)

        # PLOT CREATION

        objects = uniqueList[1:240]
        performance = uniqueCounter[1:240]
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
        embed.add_field(name="1-60", value="```" + printStringOne + "```")
        if len(printListTwo):
            embed.add_field(name="61-120", value="```" + printStringTwo + "```")
        if len(printListThree):
            embed.add_field(name="121-180", value="```" + printStringThree + "```")
        if len(printListFour):
            embed.add_field(name="181-240", value="```" + printStringFour + "```")

        message = await ctx.message.channel.send(embed=embed)

        await ctx.message.channel.send("All time shop chart", file=discord.File('shoplogs/shopchart.png'))

def setup(client):
    client.add_cog(shopcharts(client))
