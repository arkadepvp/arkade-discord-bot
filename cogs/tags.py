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
    @commands.has_any_role('Arkade Admin', 'Moderator', 'Community Mentor')
    async def tag(self, ctx, search=None):
        await ctx.message.delete()

        if search is None:
            embed = discord.Embed(title="ERROR", description="No tag specified.", color=0xFF0000)
        else:
            for tag in tags:
                if search.lower() in tag.lower():
                    tagvars = tags[tag]
                    embed = discord.Embed(title=tagvars['title'], description=tagvars['desc'], color=0x589BFF)
                    if tagvars['image'] is not "":
                        embed.set_image(url=tagvars['image'])
                    for field in tagvars['fields']:
                        if field['title'] is not "":
                            embed.add_field(name=field['title'], value=field['value'])
                    break
                else:
                    embed = discord.Embed(title="ERROR", description="No results found for: `" + search + "`", color=0xFF0000)

        message = await ctx.message.channel.send(embed=embed)

    # tags commands
    @commands.command(aliases=['listtags', 'tagslist'])
    @commands.has_any_role('Arkade Admin', 'Moderator', 'Community Mentor')
    async def tags(self, ctx):
        await ctx.message.delete()

        tagString = "`-tag <query>`\n"
        for tag in tags:
            tagvars = tags[tag]
            tagString = tagString + "- " + tagvars['dispname'] + "\n"
        embed = discord.Embed(title="Available Tags List", description=tagString, color=0x589BFF)
        message = await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(info(client))
