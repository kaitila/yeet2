import discord
from discord.ext import commands

from .parent import Globals, Utils

import asyncio


class Audio(Utils):
    def __init__(self, bot):
        self.audio_player = bot.loop.create_task(self.audio_player())
        Utils.__init__(self, bot)

    async def audio_player(self):
        """
        Ongoing event loop to play the first item in {Globals.queue}

        """
        while True:
            await asyncio.sleep(1)
            if len(Globals.queue) > 0:
                try:
                    await Globals.ctx.author.voice.channel.connect()
                except: pass
                
                Globals.voice = discord.utils.get(self.bot.voice_clients, guild=Globals.ctx.guild)

                if not Globals.voice.is_playing():
                    Globals.voice.play(discord.FFmpegPCMAudio(f"{Globals.queue[0]}.mp3"))
                    await Globals.ctx.send(f'`Now playing: {Globals.queue[0]}`')
                    Globals.queue.pop()