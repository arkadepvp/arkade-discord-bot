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

class shopcharts:
    def __init__(self, client):
        self.client = client

    #shopchart command
    @commands.command(pass_context=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def shopchart(self, ctx):
        await self.client.delete_message(ctx.message)
        #COLLECT DATA

        #download from ArkadePvP server
        urllib.request.urlretrieve('ftp://root:uq2UH3tZwKBS@147.135.8.214/Servers/L1-Ragnarok/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Ragnarok.log', 'ShopLog_Ragnarok.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://root:a3Yf6qHS@147.135.9.6/Servers/L1-Aberration/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_Aberration_P.log', 'ShopLog_Aberration.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://root:uq2UH3tZwKBS@147.135.8.214/Servers/L3-Center/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_TheCenter.log', 'ShopLog_TheCenter.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://root:uq2UH3tZwKBS@147.135.8.214/Servers/L4-Island/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_TheIsland.log', 'ShopLog_TheIsland.log')
        time.sleep(.1)
        urllib.request.urlretrieve('ftp://root:a3Yf6qHS@147.135.9.6/Servers/L2-Scorched/ShooterGame/Binaries/Win64/ArkApi/Plugins/ArkShop/ShopLog_ScorchedEarth_P.log', 'ShopLog_ScorchedEarth.log')

        filenames = ['ShopLog_Ragnarok.log', 'ShopLog_Aberration.log', 'ShopLog_TheCenter.log', 'ShopLog_TheIsland.log', 'ShopLog_ScorchedEarth.log']
        with open('Combined_Log.log', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())

        with open('Combined_Log.log', 'r') as f:
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
            printListOne = printList[50:100]
            printListTwo = printList[100:150]
            printListThree = printList[150:200]
        except Exception as e:
            print(e)

        printStringOne = "\n".join(str(e) for e in printListOne)
        printStringTwo = "\n".join(str(e) for e in printListTwo)
        printStringThree = "\n".join(str(e) for e in printListThree)

        # PLOT CREATION

        objects = uniqueList[50:150]
        performance = uniqueCounter[50:150]
        y_pos = np.arange(len(objects))

        plt.figure(figsize=(40,20))
        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects, rotation='vertical')
        plt.ylabel('Number Bought')
        plt.title('Items Purchaced In Store')

        plt.savefig('shopchart.png', bbox_inches='tight')
        # END PLOT CREATION

        #SEND EMBED TO DISCORD
        embed = discord.Embed(title="Items Purchaced Chart", description="```Item        #     || Item        #```", color=0xCC33CC)
        embed.add_field(name="1-50", value="```" + printStringOne + "```")
        embed.add_field(name="51-100", value="```" + printStringTwo + "```")
        message = await self.client.send_message(ctx.message.channel, embed=embed)

        await self.client.send_file(ctx.message.channel, 'shopchart.png')

def setup(client):
    client.add_cog(shopcharts(client))
