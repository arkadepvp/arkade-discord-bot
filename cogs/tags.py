import discord
import asyncio
import json
from discord.ext import commands
from discord.ext.commands import Bot


with open('tags.json', 'r') as f:
    tags = json.load(f)


class info:
    def __init__(self, client):
        self.client = client

    # tag command
    @commands.command(aliases=['t'])
    async def tag(self, ctx, search=None):
        await ctx.message.delete()

        if search is None:
            embed = discord.Embed(title="ERROR", description="No tag specified.", color=0xFF0000)
        else:
            search = search.lower()
            for tag in tags:
                if search in tag:
                    tagvars = tags[tag]
                    embed = discord.Embed(title=tagvars['title'], description=tagvars['desc'], color=0x589BFF)
                    if tagvars['image'] is not "":
                        embed.set_image(url=tagvars['image'])
                    for field in tagvars['fields']:
                        if field['title'] is not "":
                            embed.add_field(name=field['title'], value=field['value'])
                    break
                else:
                    embed = discord.Embed(title="ERROR", description="No results found.", color=0xFF0000)

        message = await ctx.message.channel.send(embed=embed)

    # tags commands
    @commands.command(aliases=['listtags', 'tagslist'])
    async def tags(self, ctx):
        await ctx.message.delete()

        tagString = ""
        for tag in tags:
            tagString = tagString + "\n"
        print(tagString)


def setup(client):
    client.add_cog(info(client))
