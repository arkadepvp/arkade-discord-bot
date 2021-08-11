import discord
import asyncio
import time
from datetime import datetime
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import tasks, commands
from discord.ext.commands import Bot

class tracker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_admin = client.get_cog('bot_admin')
        self.sheet_tracker.start()

    def cog_unload(self):
        self.sheet_tracker.cancel()
        print('Unloaded.')

    @tasks.loop(seconds=1800)
    async def sheet_tracker(self):
        config = await self.bot_admin.read_config()

        scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name("discord-bot-321712-53a6966956d4.json", scopes)
        headers = {'Authorization': f'Bearer {credentials.get_access_token().access_token}'}

        for guild in config['guilds']:
            gid = guild['gid']
            for tracker in guild['sheet_track']:
                guild = self.client.get_guild(id = gid)
                channel = guild.get_channel(tracker['channel_id'])
                url_format = 'https://www.googleapis.com/drive/v3/files/{id}/revisions'
                document_url = url_format.format(id = tracker['document_id'])
                response = requests.get(document_url, headers=headers).json()
                response_time = response['revisions'][-1]['modifiedTime'].split('.')[0]
                old_modified = tracker['modified']
                new_modified = datetime.strptime(response_time, '%Y-%m-%dT%H:%M:%S').isoformat()

                if old_modified == None or old_modified < new_modified:
                    message = f'Checked {tracker["document_id"]} for changes, found one or more.'
                    await self.bot_admin.log(message = message)
                    print(message)

                    embed = discord.Embed(title='Spreadsheet Update!', description='An update has been detected in the following spreadsheet: \n<https://docs.google.com/spreadsheets/d/{}>', color=0xCC00FF)
                    await channel.send(embed=embed)
                    tracker['modified'] = new_modified
                    await self.bot_admin.write_config(config)
                else:
                    message = f'Checked {tracker["document_id"]} for changes, found none.'
                    await self.bot_admin.log(message = message)
                    print(message)

    @commands.command()
    async def newtracker(self, ctx, channel, document_id):
        config = await self.bot_admin.read_config()
        config, this_guild = await self.bot_admin.create_guild(config = config, gid = ctx.guild.id)
        tracker_exists = False
        channel_id = int(channel.strip('<#>'))
        if "/d/" in document_id:
            document_id = document_id.split('/d/')[1].split('/')[0]

        for tracker in this_guild['sheet_track']:
            if document_id == tracker['document_id']:
                tracker_exists = True
                tracker['channel_id'] = channel_id
                tracker['document_id'] = document_id
                tracker['modified'] = None
                embed = discord.Embed(title='Tracker Modified', description=f'https://docs.google.com/spreadsheets/d/{document_id}', color=0xCC00FF)
                await ctx.send(embed=embed)

        if tracker_exists == False:
            new_tracker = {
                'channel_id': channel_id,
                'document_id': document_id,
                'modified': None
            }
            this_guild['sheet_track'].append(new_tracker)
            embed = discord.Embed(title='Tracker Created', description=f'https://docs.google.com/spreadsheets/d/{document_id}', color=0x00FF00)
            await ctx.send(embed=embed)

        await self.bot_admin.write_config(config)

    @commands.command()
    async def trackers(self, ctx):
        config = await self.bot_admin.read_config()

        for guild in config['guilds']:
            if ctx.guild.id == guild['gid']:
                joined_trackers = ''
                for tracker in guild['sheet_track']:
                    joined_trackers += f'https://docs.google.com/spreadsheets/d/{tracker["document_id"]}\n'
                embed = discord.Embed(title='Active Trackers:', description=f'{joined_trackers}', color=0xCC00FF)
                await ctx.send(embed=embed)

    @commands.command()
    async def deletetracker(self, ctx, document_id):
        config = await self.bot_admin.read_config()

        if "/d/" in document_id:
            document_id = document_id.split('/d/')[1].split('/')[0]

        for guild in config['guilds']:
            if ctx.guild.id == guild['gid']:
                for tracker in guild['sheet_track']:
                    if tracker['document_id'] == document_id:
                        guild['sheet_track'].remove(tracker)
                        embed = discord.Embed(title='Tracker Deleted', description=f'https://docs.google.com/spreadsheets/d/{document_id}', color=0xFF0000)
                        await ctx.send(embed=embed)

        await self.bot_admin.write_config(config)

def setup(client):
    client.add_cog(tracker(client))
