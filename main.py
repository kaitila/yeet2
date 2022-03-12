import discord
from discord.ext import commands
from pytube import Search, YouTube
from dotenv import load_dotenv

import utils
from utils import Actions, Audio, Globals, Handler

import asyncio
import os
import re


os.chdir('songs')
load_dotenv()


#Main command handler
class Client(commands.Cog):
    def __init__(self, bot: commands.Bot):
        """
        Initializes class variables and creates instances of util classes
        
        """
        self.bot = bot
        self.init = False

        self.actions = Actions(bot)
        self.handler = Handler(bot)

    async def cog_before_invoke(self, ctx):
        """
        Executes on every command

        """
        Globals.ctx = ctx
        if not self.init:
            self.audio = Audio(bot)
            self.init = True
            print(f'Initialized Audio() in {ctx.guild}')

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, search):
        """
        Plays a song matching the given keywords {search}
        
        """
        if not self.handler.lib_search(search):
            await ctx.send('`No matches in the song library!`')
            title, link = self.handler.search(search)
            await ctx.send(f'`Downloading: {title}`')
            self.handler.download(link, title)
        else:
            title = self.handler.lib_search(search)
        
        self.actions.add_to_queue(title)
        await ctx.send(f'`Added to the queue: {title}`')

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        await ctx.send(self.actions.skip())

    @commands.command(name='leave')
    async def leave(self, ctx):
        try:
            await Globals.voice.disconnect()
        except: pass

    @commands.command(name='queue')
    async def queue(self, ctx):
        await ctx.send(self.actions.get_queue())


bot = commands.Bot(command_prefix='!')
bot.add_cog(Client(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} connected')


bot.run(os.getenv('TOKEN'))
