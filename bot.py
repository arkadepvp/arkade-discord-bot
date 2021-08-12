# Works with Python 3.9.5
import discord
import asyncio
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import json
import sys

with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['token']
activity = discord.Activity(type=discord.ActivityType.listening, name="-help")
client = commands.Bot(command_prefix="-", activity=activity, status=discord.Status.online)
startup_extensions = ['cogs.bot_admin', 'cogs.help', 'cogs.ticket', 'cogs.tracker']
client.remove_command('help')

def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

@client.event
async def on_ready():
    print('---\nLogged in as\nUser: ' + client.user.name + '\nID: ' + str(client.user.id) + '\n---') # prints succesful launch in console

    # IMPORT EXTENSIONS/COGS
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
            print('Loaded extension \"{}\"'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension \"{}\"\n{}'.format(extension, exc))

"""@client.event
async def on_command_error(ctx, error):
    print(f'ERROR: {error}')

    async def embed_maker(title, description):
        await ctx.send(embed=discord.Embed(title=title, description=description, color=0xff0000))

    if isinstance(error, discord.ext.commands.errors.ConversionError):
        await embed_maker(title = 'Conversion Error', description = error)
    elif isinstance(error, discord.ext.commands.errors.UserInputError):
        await embed_maker(title = 'User Input Error', description = error)
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass
    elif isinstance(error, discord.ext.commands.errors.CheckFailure):
        await embed_maker(title = 'Check Failure', description = error)
    elif isinstance(error, discord.ext.commands.errors.DisabledCommand):
        await embed_maker(title = 'Disabled Command', description = error)
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await embed_maker(title = 'Command Invoke Error', description = error)
    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await embed_maker(title = 'Command On Cooldown', description = error)
    elif isinstance(error, discord.ext.commands.errors.MaxConcurrencyReached):
        await embed_maker(title = 'Max Concurrency Reached', description = error)"""

# load cogs
@client.command()
@is_in_guild(758821185575190590)
async def load(ctx, string):
    string = 'cogs.' + string
    try:
        client.load_extension(string)
        print('Loaded extension \"{}\"'.format(string))
        await ctx.message.channel.send('Loaded extension \"{}\"'.format(string))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension \"{}\"\n{}'.format(string, exc))
        await ctx.message.channel.send('Failed to load extension \"{}\"'.format(string))

# unload cogs
@client.command()
@is_in_guild(758821185575190590)
async def unload(ctx, string):
    string = 'cogs.' + string
    try:
        client.unload_extension(string)
        print('Unloaded extension \"{}\"'.format(string))
        await ctx.message.channel.send('Unloaded extension \"{}\"'.format(string))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to unload extension \"{}\"\n{}'.format(string, exc))

# reload cogs
@client.command()
@is_in_guild(758821185575190590)
async def reload(ctx, string):
    string = 'cogs.' + string
    try:
        client.unload_extension(string)
        print('Unloaded extension \"{}\"'.format(string))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to unload extension \"{}\"\n{}'.format(string, exc))
    try:
        client.load_extension(string)
        print('Loaded extension \"{}\"'.format(string))
        await ctx.message.channel.send('Reloaded extension \"{}\"'.format(string))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension \"{}\"\n{}'.format(string, exc))
        await ctx.message.channel.send('Failed to load extension \"{}\"'.format(string))

client.run(TOKEN)
