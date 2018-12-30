import discord
import asyncio
import json
from discord.ext import commands
from discord.ext.commands import Bot

with open('configfinal.json', 'r') as f:
    config = json.load(f)

class admin:
    def __init__(self, client):
        self.client = client

    #poll command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def poll(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="📊 | Vote ✅ or ❌ on the question below.\n_ _", description=" ".join(string), color=0xCC33CC)
        message = await ctx.message.channel.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

    #ogs command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def ogs(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="OGS Information", description="You must be a tribe rep to redeem your OGS terminal.\n Tribe reps can type **`/kit OGS`** in-game to redeem their OGS terminal.\nIf you need an additional terminal (limit one per map) you can submit a ticket.", color=0xCC33CC)
        message = await ctx.message.channel.send(embed=embed)

    #rep command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def rep(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="Tribe Representative Information", description="A Tribe Rep is a trusted member of your tribe who carries the responsibility to communicate between the Admin team the rest of your tribe. Tribe Reps will be responsible for creating tickets, redeeming [SAFE] tags, and communicating with admins should an issue arrise.", color=0xCC33CC)
        embed.add_field(name="_ _\nTribe Rep Requirements", value="Please provide the following info in <#484779257202081823>. If your tribe contains 7 or more members you are eligible for a second Tribe Rep.\n```-Screenshot of your tribe management window\n-Character name in game\n-Screenshot of approval from your tribe owner (If you are not the tribe owner)\n-How you found Ark Arkade```")
        embed.add_field(name="_ _\nTribe Rep Perks/Responsibilities", value="-Being a Tribe Representative gives access to a channel in Discord specifically meant for Reps, and allows a Rep to cast a tribe vote when polls are introduced for the community to have a voice in altering specific gameplay mechanics.\n-Being a Tribe Rep also grants you the ability to open tickets to our admin team.  To open a ticket go to the <#472229135528230912> channel and follow the directions in the pinned comment.")
        message = await ctx.message.channel.send(embed=embed)

    #safe command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def safe(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="Fun with [SAFE] tags!", description="[SAFE] tags are a protection system put in place to help tribes and players who have receive excessive amounts of structure damage or loss of creatures due to a raid recover. Tribes will be granted 100% damage protection with in a region around there base for a limited amount of time. Each safe tag is judged on a case by case basics and the time awarded is based on the damage received.", color=0xCC33CC)
        embed.add_field(name="Safe Tag Rules", value="Please read over our safe tag rules at <#509312769385037824>. Violating these rules can result in the reduction or removal of your safe tag.")
        embed.add_field(name="Safe Tag Requirements", value="Tribe Reps can create a ticket in <#472229135528230912> with the following info to request a [SAFE] tag.```-Which map your base is on and approximate coordinates\n-Screenshots of tribe-log showing as much destruction as you can\n-Pictures of the damage```")
        message = await ctx.message.channel.send(embed=embed)

    #servers command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def servers(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="Server Direct Connect Links", description="-", color=0xCC33CC)
        embed.add_field(name="PVP Server Links", value="✦ Extinction: " + config['pvpext'] + "\n✦ Ragnarok: " + config['pvprag'] + "\n✦ Aberration: " + config['pvpabb'] + "\n✦ The Center: " + config['pvpcen'] + "\n✦ The Island: " + config['pvpisl'] + "\n✦ Scorched Earth: " + config['pvpsch'] + "\n")
        embed.add_field(name="PVE Server Links", value="✦ Extinction: " + config['pveext'] + "\n✦ Ragnarok: " + config['pverag'] + "\n✦ Aberration: " + config['pveabb'] + "\n✦ The Island: " + config['pveisl'] + "\n")
        embed.add_field(name="Event Server Links", value="✦ Event Map: " + config['event1'] + "\n")
        message = await ctx.message.channel.send(embed=embed)

    #multipoll command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def multipoll(self, ctx, *string):
        await ctx.message.delete()

        pollList = list(string)
        multiList = ['?', '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭']

        try:
            pollList[1] = "🇦 " + pollList[1]
            pollList[2] = "🇧 " + pollList[2]
            pollList[3] = "🇨 " + pollList[3]
            pollList[4] = "🇩 " + pollList[4]
            pollList[5] = "🇪 " + pollList[5]
            pollList[6] = "🇫 " + pollList[6]
            pollList[7] = "🇬 " + pollList[7]
            pollList[8] = "🇭 " + pollList[8]
        except:
            pass
        embed = discord.Embed(title="📊 | Vote on the question below.\n", description="".join(pollList[0]), color=0xCC33CC)
        embed.add_field(name="---", value="\n".join(pollList[1:]))

        message = await ctx.message.channel.send(embed=embed)

        for i in range(1,len(pollList)):
            await message.add_reaction(multiList[i])

    #welcome command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def welcome(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(title="Welcome to Arkade!", description="**A PvP and PvE ARK community.**\n---", color=0xCC33CC)
        embed.set_image(url="https://cdn.discordapp.com/attachments/461022949798051871/472549308454010880/arkadebanner23.png")
        embed.add_field(name="Rates", value="✦ EXP: 3x\n✦ Gathering: 5x\n✦ Taming: 7x\n✦ Breeding: 10x (15x PvE)\n✦ Character Level: 105 +30\n✦ Wild Dino Level: 150", inline="true")
        embed.add_field(name="Links", value="✦ [Our Website](" + config['website'] + ")\n✦ [Donate](" + config['donate'] + ")\n✦ [Guilded](" + config['guilded'] + ")\n✦ [Discord](" + config['discord'] + ")\n✦ [Twitch](" + config['twitch'] + ")", inline="true")
        embed.add_field(name="_ _", value="_ _")
        embed.add_field(name="Quick Information", value="✦ Please read <#509312769385037824> or <#525499381789491201> for our rules/config.\n✦ Check <#472558681687457792> for our connect and vote links.\n✦ Ping *@Arkade Admin* in <#472623301290622993> if there is a server crash.")
        embed.add_field(name="_ _", value="_ _")
        embed.add_field(name="PVP Server Links", value="✦ Extinction: " + config['pvpext'] + "\n✦ Ragnarok: " + config['pvprag'] + "\n✦ Aberration: " + config['pvpabb'] + "\n✦ The Center: " + config['pvpcen'] + "\n✦ The Island: " + config['pvpisl'] + "\n✦ Scorched Earth: " + config['pvpsch'] + "\n")
        embed.add_field(name="_ _", value="_ _")
        embed.add_field(name="PVE Server Links", value="✦ Extinction: " + config['pveext'] + "\n✦ Ragnarok: " + config['pverag'] + "\n✦ Aberration: " + config['pveabb'] + "\n✦ The Island: " + config['pveisl'] + "\n")
        embed.add_field(name="_ _", value="_ _")
        embed.add_field(name="Event Server Links", value="✦ Event Map: " + config['event1'] + "\n")
        message = await ctx.message.channel.send(embed=embed)

def setup(client):
    client.add_cog(admin(client))
