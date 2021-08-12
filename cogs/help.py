import discord
import asyncio
import json
from discord.utils import get
from discord.ext import tasks, commands
from discord.ext.commands import Bot

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_admin = client.get_cog('bot_admin')
        with open('commands.json', 'r') as f:
            self.commands = json.load(f)

    @commands.command()
    async def admin_roles(self, ctx):
        def check(message):
            return ctx.message.author == message.author # ensures the bot only moves forward with ticketconfig if original author responds

        config = await self.bot_admin.read_config()
        config, this_guild = await self.bot_admin.create_guild(config = config, gid = ctx.guild.id)

        questions = ('Level 1?',
                     'Level 2?',
                     'Level 3?')
        responses = []

        for question in questions:
            await ctx.send(embed=discord.Embed(description=question, color=0x589BFF))
            responses.append((await self.client.wait_for('message', check=check)).content)

        for i, role in enumerate(responses):
            this_guild['admin_roles'][f'level_{i+1}'] = int(responses[i].strip('<@&> '))

        await self.bot_admin.write_config(config)

    @commands.command()
    async def help(self, ctx, argument=None):
        config = await self.bot_admin.read_config()
        config, this_guild = await self.bot_admin.get_guild(config = config, gid = ctx.guild.id)
        level = 0

        if this_guild is not None:
            if get(ctx.guild.roles, id=this_guild['admin_roles']['level_3']) in ctx.author.roles:
                level = 3
            elif get(ctx.guild.roles, id=this_guild['admin_roles']['level_2']) in ctx.author.roles:
                level = 2
            elif get(ctx.guild.roles, id=this_guild['admin_roles']['level_1']) in ctx.author.roles:
                level = 1

        if argument is None:
            embed = discord.Embed(title='Help', description='Try `-help <command> to get more detailed information about a specific command.\n`', color=0xCC00FF)
            for category in self.commands:
                category_title = category['category']
                category_content = []
                for command in category['commands']:
                    if level >= command['permission_level']:
                        category_content.append(command)
                if category_content:
                    commands = ''
                    for command in category_content:
                        commands += f'`{command["command"]}`\n'
                    embed.add_field(name=category_title, value=commands, inline=False)
            await ctx.send(embed=embed)
        else:
            argument = argument.lower()
            embed = discord.Embed(title=f'Could not find the command `{argument}`.', description='_ _', color=0xFF0000)
            for category in self.commands:
                for command in category['commands']:
                    if command['command'] == argument:
                        if level >= command['permission_level']:
                            description = f'Example: `{command["example"]}`\n{command["description"]}\n'
                            if command['arguments']:
                                description += '\nArguments:'
                                for argument in command['arguments']:
                                    description += f'\n`{argument["name"]}` - {argument["description"]}'
                            embed = discord.Embed(title=f'{command["command"]}', description=description, color=0xCC00FF)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(help(client))
