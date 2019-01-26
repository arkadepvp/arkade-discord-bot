import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot

class CommandErrorHandler:
    def __init__(self, client):
        self.client = client

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        ignore = (commands.CommandNotFound, commands.UserInputError, commands.DisabledCommand)

        error = getattr(error, 'original', error)

        if isinstance(error, ignore):
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            return await ctx.send('Error: Invalid Argument')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))
