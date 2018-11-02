import discord
import asyncio
from discord.ext import commands

import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import youtube_dl
from youtube_dl import YoutubeDL

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}*'
        duration = self.player.duration
        if duration:
            fmt = fmt + '  | Duration: {0[0]}m {0[1]}s'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, client):
        self.current = None
        self.voice = None
        self.client = client
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.client.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.client.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.client.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()

class music:
    def __init__(self, client):
        self.client = client
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.client)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.client.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.client.loop.create_task(state.voice.disconnect())
            except:
                pass

    #join command
    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx):
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.client.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.client.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    #play command
    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.join)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while trying to play: ```py\n{}: {}\n```'
            await self.client.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.1
            entry = VoiceEntry(ctx.message, player)
            await state.songs.put(entry)

    #volume command
    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.client.say('Set the volume to {:.0%}'.format(player.volume))

    #pause command
    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        #Pauses the currently played song
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    #resume command
    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        #Resumes the currently played song
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    #stop command
    @commands.command(pass_context=True, no_pm=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def stop(self, ctx):
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    #skip command
    @commands.command(pass_context=True, no_pm=True)
    @commands.has_any_role('Arkade Admin', 'Moderator')
    async def skip(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.client.say('Nothing is playing.')
            return

        await self.client.say('Song skipped.')
        state.skip()

    #playing
    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.client.say('Nothing is playing.')
        else:
            skip_count = len(state.skip_votes)
            await self.client.say('Now playing {}'.format(state.current, skip_count))

def setup(client):
    client.add_cog(music(client))
