import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord import opus

class music:
    def __init__(self, client):
        self.client = client
		
    #play command
    @commands.command(pass_context=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def play(self, ctx, url):
        if voice_client:
            await voice_client.disconnect()
        else: 
	        pass
        author = ctx.message.author
        voice_channel = author.voice_channel
        vc = await self.client.join_voice_channel(voice_channel)

        player = await vc.create_ytdl_player(url)
        player.volume = 0.10
        player.start()

    #fire command
    @commands.command(pass_context=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def fire(self, ctx):
        if voice_client:
            await voice_client.disconnect()
        else: 
            pass

        author = ctx.message.author
        voice_channel = author.voice_channel
        vc = await self.client.join_voice_channel(voice_channel)

        player = await vc.create_ytdl_player("https://www.youtube.com/watch?v=9LssTi4X8jY")
        player.volume = 1.00
        player.start()

    #stream command
    @commands.command(pass_context=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def stream(self, ctx, url):
        author = ctx.message.author
        voice_channel = author.voice_channel
        vc = await self.client.join_voice_channel(voice_channel)

        player = await vc.create_ytdl_player(url, stream=True)
        player.volume = 0.10
        player.start()

    #stop command
    @commands.command(pass_context=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def stop(self, ctx):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        if voice_client:
            await voice_client.disconnect()
        else:
            self.client.say("I was not playing anything!")

def setup(client):
    client.add_cog(music(client))
