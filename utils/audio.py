import discord
from discord.ext import commands

from utils import Utils

import asyncio


class Audio(Utils):
    def __init__(self, bot, ctx):
        self.audio_player = bot.loop.create_task(self.audio_player())
        Utils.__init__(self, bot, ctx)

    async def audio_player(self):
        """
        Ongoing event loop to play the first item in queue

        """
        while True:
            await asyncio.sleep(1)
            if len(self.queue[self.ctx.guild.id]) > 0:
                try:
                    await self.ctx.author.voice.channel.connect()
                    #self.voice = discord.utils.get(self.bot.voice_clients, guild=self.ctx.guild)
                except: pass

                self.voice = discord.utils.get(self.bot.voice_clients, guild=self.ctx.guild)

                if not self.voice.is_playing():
                    self.voice.play(discord.FFmpegPCMAudio(f"{self.queue[self.ctx.guild.id][0]}.mp3"))
                    await self.ctx.send(f'`Now playing: {self.queue[self.ctx.guild.id][0]}`')
                    self.queue[self.ctx.guild.id].pop()