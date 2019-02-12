import discord
import asyncio
import json
import math
from discord.ext import commands
from discord.ext.commands import Bot

with open('configfinal.json', 'r') as f:
    config = json.load(f)


class admin:
    def __init__(self, client):
        self.client = client

    # poll command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def poll(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="📊 | Vote ✅ or ❌ on the question below.\n_ _", description=" ".join(string), color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

    # sqrt command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def sqrt(self, ctx, time: float):
        addedTime = round((2*(math.sqrt(time))), 1)
        totalTime = addedTime + time
        message = await ctx.message.channel.send(f"The increase in ban time should be: {addedTime} The new total ban time should be: {totalTime}")

    # ogs command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def ogs(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="OGS Information", description="You must be a tribe rep to redeem your OGS terminal.\n Tribe reps can type **`/kit ogs`** in-game to redeem their OGS terminal.\nIf you need an additional terminal (limit one per map) you can submit a ticket.", color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)

    # rep command
    @commands.command(aliases=['triberep', 'reps'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def rep(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="Tribe Representative Information", description="A Tribe Rep is a trusted member of your tribe who carries the responsibility to communicate between the Admin team the rest of your tribe. Tribe Reps will be responsible for creating tickets, redeeming [Safe] tags, and communicating with admins should an issue arrise.", color=0xFF00FF)
        embed.add_field(name="_ _\nTribe Rep Requirements", value="Please provide the following info in <#535668637877534740>. If your tribe contains 6 or more members you are eligible for a second Tribe Rep.\n```-Screenshot of your tribe management window\n-Character name in game\n-Screenshot of approval from your tribe owner (If you are not the tribe owner)\n-How you found Ark Arkade```")
        embed.add_field(name="_ _\nTribe Rep Perks/Responsibilities", value="-Being a Tribe Representative gives access to a channel in Discord specifically meant for Reps, and allows a Rep to cast a tribe vote when polls are introduced for the community to have a voice in altering specific gameplay mechanics.\n-Being a Tribe Rep also grants you the ability to open tickets to our admin team.  To open a ticket go to the <#472229135528230912> channel and follow the directions in the pinned comment.")
        message = await ctx.message.channel.send(embed=embed)

    # webhook command
    @commands.command(aliases=['wh', 'hook', 'web', 'showmewebhook!', 'wewantwebhooks'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def webhook(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="Webhook Tutorial", description="https://arkade.flowlu.com/hc/5/74--discord-tribelog-webhook", color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)

    # [Safe] command
    @commands.command(aliases=['st', 'safetag', 'tag'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def safe(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="Fun with [Safe] tags!", description="[SAFE] tags are a protection system put in place to help tribes and players who have receive excessive amounts of structure damage or loss of creatures due to a raid recover. Tribes will be granted 100% damage protection with in a region around there base for a limited amount of time. Each [Safe] tag is judged on a case by case basics and the time awarded is based on the damage received.", color=0xFF00FF)
        embed.add_field(name="Safe Tag Rules", value="Please read over our [Safe] tag rules at <#535273670919323648>. Violating these rules can result in the reduction or removal of your [Safe] tag.")
        embed.add_field(name="Safe Tag Requirements", value="Tribe Reps can create a ticket in <#472229135528230912> with the following info to request a [Safe] tag.```-Which map your base is on and approximate coordinates\n-Screenshots of tribe-log showing as much destruction as you can\n-Pictures of the damage```")
        message = await ctx.message.channel.send(embed=embed)

    # saferules command
    @commands.command(aliases=['sr', 'safetagrules', 'saferule'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def safe(self, ctx, int=None):
        await ctx.message.delete()
        if int is None:
            embed = discord.Embed(title="[SAFE] tag Rules", description="You've been granted a [Safe] tag. Please do not pick up and move your OGS terminal while you [Safe] tag is active. This will cancel your [Safe] tag and an admin will not reset it. Please remember that all structures inside the [Safe] bubble are protected, but your dinos are not. Make sure you read the following [Safe] tag rules and punishments.", color=0xFF00FF)
        else:
            embed = discord.Embed(title="[SAFE] tag Rules", description="You've been granted " + int + " hours for your [Safe] tag. Please do not pick up and move your OGS terminal while you [Safe] tag is active. This will cancel your [Safe] tag and an admin will not reset it. Please remember that all structures inside the [Safe] bubble are protected, but your dinos are not. Make sure you read the following [Safe] tag rules and punishments.", color=0xFF00FF)

        embed.add_field(name="[Safe] tag rules.", value="```◈ While under the effects of the [Safe] Tag protection, tribes are not allowed to raid or destroy any other tribes structures across all maps, but any other forms of PvP are acceptable.\n◈ No impeding of [Safe] Tribes around their protection bubble.\n◈ It is the responsibility of the tribe owner to remove the [Safe] tag from the tribes name at the end of the [Safe] Tag protection.```")
        embed.add_field(name="[Safe] Tag Punishments", value="```Breaking any of the [Safe] Tag rules and guidelines will have punishments associated with the [Safe] Tag system. These punishments could include, but are not limited to:\n◈ A reduction or removal of your current [Safe] Tag.\n◈ Reduced time or no [Safe] Tag offered in future scenarios.\n◈ Players kicked/banned for a period of time.```")
        message = await ctx.message.channel.send(embed=embed)

    # sellable command
    @commands.command(aliases=['sell'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def sellable(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="Sellable Resource", description="The \"sellable\" resource is no longer used on ARKADE. last season it was used to transfer coins between maps, but now the shop is cluster wide and coins transfer automatically!", color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)

    # wipe command
    @commands.command(aliases=['wipedate', 'wiping'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def wipe(self, ctx, *string):
        await ctx.message.delete()

        embed = discord.Embed(title="Server Wipes", description="The last PvP wipe was on `1/18`.  ARKADE does not operate under a set wipe schedule.  A wipe will generally be considered approximately every 2-3 months when gameplay tends to start getting stagnant and a cluster rejuvenation is deemed to be beneficial to the player population.  A wipe is not being considered at this time.\n\nThe PvE servers do not wipe.", color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)

    # servers command
    @commands.command(aliases=['server'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def servers(self, ctx, *string):
        await ctx.message.delete()
        pvpServers = ""
        pveServers = ""
        eventServers = ""

        for server in config['arkPvpServers']:
            pvpServers = pvpServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"

        for server in config['arkPveServers']:
            pveServers = pveServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"

        for server in config['arkEventServers']:
            eventServers = eventServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"

        embed = discord.Embed(title="Server Direct Connect Links", description="-", color=0xFF00FF)
        embed.add_field(name="PVP Server Links", value=pvpServers)
        embed.add_field(name="PVE Server Links", value=pveServers)
        embed.add_field(name="Event Server Links", value=eventServers)
        message = await ctx.message.channel.send(embed=embed)

    # multipoll command
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
        embed = discord.Embed(title="📊 | Vote on the question below.\n", description="".join(pollList[0]), color=0xFF00FF)
        embed.add_field(name="---", value="\n".join(pollList[1:]))

        message = await ctx.message.channel.send(embed=embed)

        for i in range(1, len(pollList)):
            await message.add_reaction(multiList[i])

    # welcome command
    @commands.command()
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def welcome(self, ctx):
        await ctx.message.delete()
        links = ""
        pvpServers = ""
        pveServers = ""
        eventServers = ""
        for link in config['links']:
            links = links + "✦ " + "[" + link['Title'] + "](" + link['URL'] + ")\n"
        for server in config['arkPvpServers']:
            pvpServers = pvpServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"
        for server in config['arkPveServers']:
            pveServers = pveServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"
        for server in config['arkEventServers']:
            eventServers = eventServers + "✦ " + server['Map'] + ": " + server['IP'] + "\n"

        embed = discord.Embed(title="Welcome to Arkade!", description="**A PvP and PvE ARK community.**\n\u200b\n", color=0xFF00FF)
        embed.add_field(name="Rates", value="✦ EXP: 3x\n✦ Gathering: 5x\n✦ Taming: 7x\n✦ Breeding: 10x (15x PvE)\n✦ Character Level: 105 +30\n✦ Wild Dino Level: 150\n\u200b\n", inline="true")
        embed.add_field(name="Links", value=links, inline="true")
        embed.add_field(name="Quick Information", value="✦ Please read <#535273670919323648> or <#525499381789491201> for our rules/config.\n✦ Check <#472558681687457792> for our connect and vote links.\n✦ Ping *@Arkade Admin* in <#472623301290622993> if there is a server crash.\n\u200b\n")
        embed.add_field(name="PVP Server Links", value=pvpServers)
        embed.add_field(name="PVE Server Links", value=pveServers)
        embed.add_field(name="Event Server Links", value=eventServers)
        embed.add_field(name="Self Assignable Roles", value="Add your reaction to any of the available role options that you want to join.\nSelecting a role will give you access to the relevant discussion channels in this Discord server.  You may choose more than one role.\n\n**ARK PvP: **:bow_and_arrow:\n**ARK PvE: **:hammer:")
        welcomeMsg = await ctx.channel.get_message(527842025329131521)
        message = await welcomeMsg.edit(embed=embed)

    # flowlu command
    @commands.command(aliases=['flow', 'knowledgebase', 'f'])
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def flowlu(self, ctx, string='empty'):
        await ctx.message.delete()

        if 'webhook' in string.lower():
            embed = discord.Embed(title="Flowlu - Webhook", description="https://arkade.flowlu.com/hc/5/74--discord-tribelog-webhook", color=0xFF00FF)
        elif 'connect' in string.lower():
            embed = discord.Embed(title="Flowlu - Player Already Connected", description="https://arkade.flowlu.com/hc/5/17-19--another-player-connected", color=0xFF00FF)
        elif 'mismatch' in string.lower():
            embed = discord.Embed(title="Flowlu - Mod Mismatch", description="https://arkade.flowlu.com/hc/5/17-15--mod-mismatch-error", color=0xFF00FF)
        elif 'transfer' in string.lower():
            embed = discord.Embed(title="Flowlu - Can't Transfer", description="https://arkade.flowlu.com/hc/5/17-16--not-seeing-arkade-servers-on-cluster", color=0xFF00FF)
        elif 'buffer' in string.lower():
            embed = discord.Embed(title="Flowlu - Buffer Overflow", description="https://arkade.flowlu.com/hc/5/17-18--overflow-buffer-error-upon-transferring", color=0xFF00FF)
        elif 'kits' in string.lower():
            embed = discord.Embed(title="Flowlu - Kits", description="https://arkade.flowlu.com/hc/5/73-29--arkade-kits", color=0xFF00FF)
        elif 'rank' in string.lower():
            embed = discord.Embed(title="Flowlu - Tribe Ranks and You", description="https://arkade.flowlu.com/hc/5/95--tribe-ranks-and-you", color=0xFF00FF)
        elif 'screenshot' in string.lower():
            embed = discord.Embed(title="Flowlu - Easy Screenshots", description="https://arkade.flowlu.com/hc/5/42--easy-screen-shots", color=0xFF00FF)
        elif 'empty' in string.lower():
            embed = discord.Embed(title="Flowlu - Error", description="Invalid article. Choose from the following.\n- Webhook\n- Player Already Connected\n- Mismatch\n- Can't Transfer\n- Buffer Overflow\n- Kits\n-Tribe Ranks\n- Screenshots", color=0xFF0000)

        message = await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(admin(client))
