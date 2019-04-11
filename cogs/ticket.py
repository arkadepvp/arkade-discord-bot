import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot


class ticket:
    def __init__(self, client):
        self.client = client

    async def on_guild_channel_update(self, before, after):
        if after.category_id in [473652853354004480, 533147428715495434, 533752291853860864]:
            if "are" in after.name[0:4]:
                areCategory = discord.utils.get(after.guild.categories, id=533147428715495434)
                await after.edit(category=areCategory, topic="ARK PvE Ticket")
                print("Ticket moved to PvE with ID: " + str(areCategory.id))
            elif "arp" in after.name[0:4]:
                arpCategory = discord.utils.get(after.guild.categories, id=533752291853860864)
                await after.edit(category=arpCategory, topic="ARK PvP Ticket")
                print("Ticket moved to PvP with ID: " + str(arpCategory.id))

    async def on_guild_channel_create(self, ticket):
        embed = discord.Embed(title="Thank you for opening a ticket.", description="Please react to this message with the cluster this ticket pertains to.\n\n**ARK PvP: **:bow_and_arrow:\n**ARK PvE: **:hammer:\n**ARK 6Man: **:six:"", color=0xFF00FF)
        message = await ctx.message.channel.send(embed=embed)

        await client.add_reaction(message, 	"\U0001F3F9")
        await client.add_reaction(message, 	"\U0001F528")
        await client.add_reaction(message, 	"\U0001F3F9")


def setup(client):
    client.add_cog(ticket(client))
