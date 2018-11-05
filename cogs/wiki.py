import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from lxml import html
import requests
import sys

class wiki:
    def __init__(self, client):
        self.client = client

    #tame command
    @commands.command()
    async def two(self, ctx):
        await self.client.delete_message(ctx.message)

        embed = discord.Embed(title="Arkade PvP Bot Information:", description="_ _", color=0x50bdfe)
        embed.add_field(name='Command', value="```%info\n%poll <arg>\n \n%cmd```", inline=True)
        embed.add_field(name='Description', value="```Shows this page.\nStarts a poll with the question: <arg>.\ncmddesc```", inline=True)
        embed.add_field(name='_ _', value="-------------------------------------------------------------------------------------------------")
        message = await ctx.message.channel.send(embed=embed)

    #craft command
    @commands.command()
    async def craft(self, ctx, string, extend = None):
        string = string.capitalize()
        stringSafeThumb = string
        if extend:
            extendFix = extend.capitalize()
            string = string + "_" + extendFix
        else:
            pass

        url = "https://ark.gamepedia.com/{0}".format(string)
        page = requests.get(url)
        tree = html.fromstring(page.content)

        stringSafeThumb = stringSafeThumb.rstrip("s")
        thumb = ("".join(tree.xpath('//img[starts-with(@alt, "%s")]/@src'%stringSafeThumb))).split("?", 1)[0]
        level = ("".join(tree.xpath('//a[@href="/Levels"]/following-sibling::text()[1]'))).rstrip("\n")
        cost_item = (("\n,".join(tree.xpath('//div[@style="display:inline-block;margin:0.2em 1em 0.2em 0;vertical-align:top;text-align:left"]/div/b/a[position() mod 2 = 0]/@href'))).replace("/", "")).replace("_", " ")
        cost_quantity = ",".join(tree.xpath('//div[@style="display:inline-block;margin:0.2em 1em 0.2em 0;vertical-align:top;text-align:left"]/div/b[position() mod 2 = 1]/text()[position() mod 2 = 1]'))
        cost_item = cost_item.split(",")
        cost_quantity = cost_quantity.split(",")

        cost = [None]*(len(cost_quantity)+len(cost_item))
        cost[::2] = cost_quantity
        cost[1::2] = cost_item

        embed = discord.Embed(title="{0}".format(string), url=url, color=0xffff66)

        embed.set_thumbnail(url=thumb)
        embed.add_field(name='Required Level: ', value="Level{0}".format(level))
        embed.add_field(name='Required Resources: ', value=" " + "".join(cost))
        embed.set_footer(text="Information from ark.gamepedia.com", icon_url="https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/b/bc/Wiki.png")
        try:
            message = await ctx.message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Error", description="That is not a valid craft.", color=0xff0000)
            message = await ctx.message.channel.send(embed=embed)

    #search command
    @commands.command()
    async def search(self, ctx, *string):
        search = "+".join(string)
        url = "https://ark.gamepedia.com/index.php?search={0}&title=Special%3ASearch&fulltext=Search".format(search)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        try:
            searchResult = tree.xpath('//ul[@class="mw-search-results"]/li/div/a/@href[1]')
            searchUrl = "https://ark.gamepedia.com" + searchResult[0]
            embed = discord.Embed(title="Ark Gamepedia: " + (searchResult[0]).strip("/"), url=searchUrl, color=0xffff66)
        except:
            embed = discord.Embed(title="Ark Gamepedia: No Results Found", color=0xff0000)
        embed.set_footer(text="Information from ark.gamepedia.com", icon_url="https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/b/bc/Wiki.png")
        message = await ctx.message.channel.send(embed=embed)

    #map command
    @commands.command()
    async def map(self, ctx, string, extend = None):
        if (string.lower()).startswith("isl"):
            mapUrl = "https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/0/04/The_Island_Topographic_Map.jpg"
            embed = discord.Embed(title="Island map: ", color=0xffff66)
        elif (string.lower()).startswith("cen"):
            mapUrl = "https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/thumb/5/58/The_Center_Topographic_Map.jpg/800px-The_Center_Topographic_Map.jpg?"
            embed = discord.Embed(title="Center map: ", color=0xffff66)
        elif (string.lower()).startswith("ab"):
            mapUrl = "https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/2/20/Map_Aberration.png"
            embed = discord.Embed(title="Aberration map: ", color=0xffff66)
        elif (string.lower()).startswith("rag"):
            mapUrl = "https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/thumb/c/cf/Ragnarok_Ocean_Topographic_Map.jpg/800px-Ragnarok_Ocean_Topographic_Map.jpg?"
            embed = discord.Embed(title="Ragnarok map: ", color=0xffff66)
        elif (string.lower()).startswith("sco"):
            mapUrl = "https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/3/39/Scorched_Earth_Topographic_Map.jpg"
            embed = discord.Embed(title="Scorched map: ", color=0xffff66)
        elif (string.lower()).startswith("ext"):
            mapUrl = "https://png2.kisspng.com/sh/c8e2de65018473ce38648b4c0211a2a4/L0KzQYm3VsI6N6t9gpH0aYP2gLBuTfVud5tuRdd2b4Tsc7F1TgNucZ1qkZ9sbHnzPbL5lL1pdZ4yTdQ8NkjoSYm9UcIyPWUzTKo6NEO4QYK4VcMxO2E3SaI9M0m6SXB3jvc=/kisspng-emoji-emoticon-smiley-clip-art-hmm-5b368e98612154.4814351115303021043979.png"
            embed = discord.Embed(title="Extinction map: ", color=0xffff66)
        else:
            embed = discord.Embed(title="Error", description="That is not a valid map.", color=0xff0000)
            mapUrl = ""

        if mapUrl:
            embed.set_image(url=mapUrl)
        else:
            pass
        embed.set_footer(text="Information from ark.gamepedia.com", icon_url="https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/b/bc/Wiki.png")
        message = await ctx.message.channel.send(embed=embed)

    #wiki command
    @commands.command()
    async def wiki(self, ctx, string, extend = None):
        string = string.capitalize()
        stringSafeThumb = string
        if extend:
            extendFix = extend.capitalize()
            string = string + "_" + extendFix
        else:
            pass

        url = "https://ark.gamepedia.com/{0}".format(string)
        page = requests.get(url)
        tree = html.fromstring(page.content)

        thumb = ("".join(tree.xpath('(//img[starts-with(@alt, "Dossier")]/@src)[2]'))).rstrip("\n")
        species = ("".join(tree.xpath('//div/div/div/i/text()'))).rstrip("\n")
        diet = ("".join(tree.xpath('(//div/div/div/a[starts-with(@href, "/Category")]/text())[1]'))).rstrip("\n")
        temperment = ("".join(tree.xpath('(//div/div/div[@class="info-arkitex-right info-X2-60"]/text())[3]'))).rstrip("\n")
        tameable = (("".join(tree.xpath('//div[1]/div[@class="info-arkitex info-unit-row"][2]/div[@class="info-arkitex-left info-X3-33"]/text()'))).rstrip("\n")).strip("\n")
        rideable = (("".join(tree.xpath('//div[1]/div[@class="info-arkitex info-unit-row"][2]/div[@class="info-X3-33"]/text()'))).rstrip("\n")).strip("\n")
        breedable = (("".join(tree.xpath('//div[1]/div[@class="info-arkitex info-unit-row"][2]/div[@class="info-arkitex-right info-X3-33"]/text()'))).rstrip("\n")).strip("\n")

        embed = discord.Embed(title="{0}".format(string), url=url, color=0xffff66)

        embed.set_thumbnail(url=thumb)
        embed.add_field(name="Species", value="*" + species + "*", inline=True)
        embed.add_field(name="Diet", value=diet, inline=True)
        embed.add_field(name="Temperment", value=temperment, inline=True)
        embed.add_field(name="Tameable", value=tameable, inline=True)
        embed.add_field(name="Rideable", value=rideable, inline=True)
        embed.add_field(name="Breedable", value=breedable, inline=True)
        embed.add_field(name="_ _", value="_ _", inline=False)
        embed.add_field(name="Dossier", value="TBD", inline=False)
        embed.set_footer(text="Information from ark.gamepedia.com", icon_url="https://d1u5p3l4wpay3k.cloudfront.net/arksurvivalevolved_gamepedia/b/bc/Wiki.png")
        try:
            message = await ctx.message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Error", description="That is not a valid dinosaur.", color=0xff0000)
            message = await ctx.message.channel.send(embed=embed)

def setup(client):
    client.add_cog(wiki(client))
