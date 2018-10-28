# Works with Python 3.6+
# THIS IS THE LIVE VERSION
import discord
import asyncio
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import json

with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config['token']
client = commands.Bot(command_prefix=".")
startup_extensions = ["wiki", "music", "admin", "shoplogs"]
client.remove_command('help')
async def on_ready():
    pass

@client.event
async def on_ready():
    #sets Playing message on discord
    await client.change_presence(game=Game(name="N0X Was Here | .help"))
    #prints succesful launch in console
    print('---\nLogged in as\nUser: ' + client.user.name + '\nID: ' + client.user.id + '\n---')

    #sets up react message
    ragnarok = get(client.get_all_emojis(), name='ragnarok')
    aberration = get(client.get_all_emojis(), name='aberration')
    center = get(client.get_all_emojis(), name='center')
    island = get(client.get_all_emojis(), name='island')
    scorched = get(client.get_all_emojis(), name='scorched')

    reactChannel = client.get_channel('493261000330575872')
    text = "```md\nReact to join server groups.\n===========================\nRag, Ab, Center, Island, Scorched```"
    message = await client.send_message(reactChannel, text)

    await client.add_reaction(message, ragnarok)
    await client.add_reaction(message, aberration)
    await client.add_reaction(message, center)
    await client.add_reaction(message, island)
    await client.add_reaction(message, scorched)
    #finish react message

# adds roles based on reaction
@client.event
async def on_reaction_add(reaction, user):
    channel = '493261000330575872'

    ragnarok = get(client.get_all_emojis(), name='ragnarok')
    aberration = get(client.get_all_emojis(), name='aberration')
    center = get(client.get_all_emojis(), name='center')
    island = get(client.get_all_emojis(), name='island')
    scorched = get(client.get_all_emojis(), name='scorched')

    if reaction.message.channel.id != channel:
        return
    if reaction.emoji == ragnarok:
        role = get(user.server.roles, name="Ragnarok")
        await client.add_roles(user, role)
    elif reaction.emoji == aberration:
        role = get(user.server.roles, name="Aberration")
        await client.add_roles(user, role)
    elif reaction.emoji == center:
        role = get(user.server.roles, name="Center")
        await client.add_roles(user, role)
    elif reaction.emoji == island:
        role = get(user.server.roles, name="Island")
        await client.add_roles(user, role)
    elif reaction.emoji == scorched:
        role = get(user.server.roles, name="Scorched")
        await client.add_roles(user, role)

#removes roles based on reaction
@client.event
async def on_reaction_remove(reaction, user):
    channel = '493261000330575872'

    ragnarok = get(client.get_all_emojis(), name='ragnarok')
    aberration = get(client.get_all_emojis(), name='aberration')
    center = get(client.get_all_emojis(), name='center')
    island = get(client.get_all_emojis(), name='island')
    scorched = get(client.get_all_emojis(), name='scorched')

    if reaction.message.channel.id != channel:
        return
    if reaction.emoji == ragnarok:
        role = get(user.server.roles, name="Ragnarok")
        await client.remove_roles(user, role)
    elif reaction.emoji == aberration:
        role = get(user.server.roles, name="Aberration")
        await client.remove_roles(user, role)
    elif reaction.emoji == center:
        role = get(user.server.roles, name="Center")
        await client.remove_roles(user, role)
    elif reaction.emoji == island:
        role = get(user.server.roles, name="Island")
        await client.remove_roles(user, role)
    elif reaction.emoji == scorched:
        role = get(user.server.roles, name="Scorched")
        await client.remove_roles(user, role)

#help command
@client.command(pass_context=True)
async def help(ctx):
    await client.delete_message(ctx.message)

    embed = discord.Embed(title="Help: ", description="Command arguments are shown with <> and are required.\n", color=0x50bdfe)
    embed.add_field(name="General Commands", value="`.help` -  Displays this information\n`.info` - Displays info about the bot")
    embed.add_field(name="Ark Commands", value="`.craft <>` -  Display crafting requirments for an item\n`.search <>` -  Searches [gamepedia](https://ark.gamepedia.com) for the given query\n`.map <>` -  Displays a picture of the given map.\n`.tame <>` -  In development.\n`.wiki <>` -  Displays basic wiki info of the given dinosaur")
    if ctx.message.author.server_permissions.administrator:
        embed.add_field(name="Admin Commands", value="`.poll <>` - Creates a poll with the given question\n`.welcome` - Sends the welcome message in the active channel\n`.play` - Plays a youtube link (must be in a voice channel)\n`.fire` - A nice relaxing fireplace (mst be in a voice channel)\n`.stop` - Stops whatever is currently playing")
    message = await client.send_message(ctx.message.channel, embed=embed)

#info command
@client.command(pass_context=True)
async def info(ctx):
    await client.delete_message(ctx.message)

    embed = discord.Embed(title="Arkade PvP Bot Information", description="A custom built bot for the [Arkade PvP Discord.](https://discord.gg/G8d5YFd)", color=0x50bdfe)
    embed.set_thumbnail(url="https://s3-us-west-2.amazonaws.com/www.guilded.gg/user_content/image/de968c2d-8f58-4778-f007-720acab23e3e.png")
    embed.add_field(name="_ _", value="_ _")
    embed.add_field(name="_ _", value="made with love by<@147901548167430144>")
    message = await client.send_message(ctx.message.channel, embed=embed)

#IMPORT EXTENSIONS/COGS
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension \"{}\n{}\"'.format(extension, exc))
#DONE IMPORT EXTENSIONS/COGS

client.run(TOKEN)
