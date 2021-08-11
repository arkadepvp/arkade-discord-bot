import discord
import asyncio
import time
import json
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot

with open('config.json', 'r') as f:
    config = json.load(f)

class TicketButtons(discord.ui.Button['TicketCreator']):
    def __init__(self, ticketCategory, y: int):
        super().__init__(style=discord.ButtonStyle.primary, label=ticketCategory, custom_id=ticketCategory, row=y)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicketCreator = self.view

        this_guild = None
        permission_groups = []
        for guild in config['guilds']:
            if guild['gid'] == interaction.guild_id:
                this_guild = guild
                break

        for category in this_guild['ticket_config']['categories']:
            if category['title'] == self.custom_id:
                channel = await interaction.guild.create_text_channel(name=f"ticket#{this_guild['ticket_config']['ticket_id']}", category=category['id'], reason='Ticket')
        await interaction.response.send_message(content=f"{interaction.user.mention} New **{self.label}** ticket available here: {channel.mention}", ephemeral=True)

        for role_id in this_guild['ticket_config']['roles']:
            role_id = int(role_id.strip(' ')[3:-1])
            permission_groups.append(get(interaction.guild.roles, id=role_id))
        permission_groups.append(interaction.user)
        print(permission_groups)
        for permission_group in permission_groups:
            await channel.set_permissions(permission_group, read_messages=True, send_messages=True)

        this_guild['ticket_config']['ticket_id'] += 1

        # write new config settings to file.
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

class TicketCreator(discord.ui.View):
    def __init__(self):
        super().__init__()
        for i, ticketCategory in enumerate(['PvP', 'Legacy', 'Survival', 'Extreme', 'Creative', 'Discord/Other']):
            y = 0
            if i > 4: # Buttons limited to 5 per line
                y = 1
            self.add_item(TicketButtons(ticketCategory, y))

class ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_admin = client.get_cog('bot_admin')

    # ticket config command
    @commands.command()
    async def ticketconfig(self, ctx):
        def check(message):
            return ctx.message.author == message.author # ensures the bot only moves forward with ticketconfig if original author responds

        config = await self.bot_admin.read_config()
        config, this_guild = await self.bot_admin.create_guild(config = config, gid = ctx.guild.id)
        questions = ('What channel will tickets be created in?',
                     'What roles should have access to tickets? EX: @Admim, @Moderator',
                     'List the ticket types & category IDs EX: type/ID, type/ID')
        responses = []

        for question in questions:
            await ctx.send(embed=discord.Embed(description=question, color=0x589BFF))
            responses.append((await self.client.wait_for('message', check=check)).content)

        this_guild['ticket_config'] = {'ticket_id': this_guild['ticket_config']['ticket_id'],'channel': '','message': this_guild['ticket_config']['message'],'roles': [],'categories': []}
        this_guild['ticket_config']['channel'] = int(responses[0].strip('<#>'))
        for role in responses[1].split(','):
            this_guild['ticket_config']['roles'].append(int(role.strip('<@&> ')))
        for category in responses[2].split(', '):
            split_category = category.rsplit('/',1)
            ticket_categories = {'title': split_category[0], 'id': int(split_category[1])}
            this_guild['ticket_config']['categories'].append(ticket_categories)

        guild = self.client.get_guild(this_guild['gid'])
        channel = guild.get_channel(this_guild['ticket_config']['channel'])
        if this_guild['ticket_config']['message'] is not None:
            message = await channel.fetch_message(this_guild['ticket_config']['message'])
            await message.delete()

        message = await channel.send('Select a button to create a ticket', view=TicketCreator()) # starts tickets
        this_guild['ticket_config']['message'] = message.id
        await self.bot_admin.write_config(config) # write new config settings to file.

def setup(client):
    client.add_cog(ticket(client))
