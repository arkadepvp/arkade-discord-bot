import discord
import asyncio
import json
from discord.ext import commands
from discord.ext.commands import Bot

class bot_admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('config.json', 'r') as f:
            self.config = json.load(f)

    def is_in_guild(guild_id):
        async def predicate(ctx):
            return ctx.guild and ctx.guild.id == guild_id
        return commands.check(predicate)

    async def read_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config

    async def write_config(self, config):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    async def log(self, message):
        dev_gid = self.config['dev_gid']
        log_channel = self.config['log_channel']
        guild = self.client.get_guild(id = dev_gid)
        channel = guild.get_channel(log_channel)
        await channel.send(message)

    async def create_guild(self, config, gid):
        guild_exists = False
        this_guild = None
        for guild in config['guilds']:
            if gid == guild['gid']:
                guild_exists = True
                this_guild = guild

        if guild_exists == False:
            print(config['guilds'])
            print(gid)
            print(f'CREATING GUILD: {gid}')
            new_guild = {
                'gid': gid,
                'admin_roles': {
                },
                'ticket_config': {'ticket_id': 0,
                                  'channel': '',
                                  'message': None,
                                  'roles': [],
                                  'categories': []},
                'sheet_track': []
            }
            config['guilds'].append(new_guild)
            this_guild = config['guilds'][-1]

        await self.write_config(config)
        return config, this_guild

    async def get_guild(self, config, gid):
        this_guild = None
        for guild in config['guilds']:
            if gid == guild['gid']:
                this_guild = guild

        return config, this_guild

    # Prints config, must be in development guild
    @commands.command()
    @is_in_guild(758821185575190590)
    async def config(self, ctx):
        config = await self.read_config()
        await ctx.send(f'```json\n{json.dumps(config, indent=4)}```')

    @commands.command()
    @is_in_guild(758821185575190590)
    async def logtest(self, ctx, message):
        await self.log(message = message)

def setup(client):
    client.add_cog(bot_admin(client))
