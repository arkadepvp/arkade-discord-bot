import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class ticketsort:
    def __init__(self, client):
        self.client = client

    async def on_guild_channel_update(self, before, after):
        if after.category_id == 473652853354004480:
            print("New Ticket Created")
            if "are" in after.name:
                areCategory = discord.utils.get(after.guild.categories, id=533147428715495434)
                await after.edit(category=areCategory, topic="ARK PvE Ticket")
                print("Ticket moved to PvE with ID: " + str(areCategory.id))
            if "sc" in after.name:
                scCategory = discord.utils.get(after.guild.categories, id=533752291853860864)
                await after.edit(category=scCategory, topic="ARK SC Ticket")
                print("Ticket moved to SC with ID: " + str(scCategory.id))

def setup(client):
    client.add_cog(ticketsort(client))
