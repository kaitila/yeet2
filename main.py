import discord
from discord.ext import commands
from pytube import YouTube
from pytube import Search

import asyncio
from dotenv import load_dotenv
import os
import re

os.chdir('songs')
load_dotenv()

class Audio():
    def __init__(self, bot):
        self.bot = bot
        self.audio_player = bot.loop.create_task(self.audio_player())
        self.queue = {}

    async def audio_player(self):
        while True:
            await asyncio.sleep(2)
        
    def add_to_queue(self, title, ctx):
        try: self.queue[ctx.guild.id]
        except KeyError: self.queue[ctx.guild.id] = []

        self.queue[ctx.guild.id].append(title)
        print(self.queue)
        

    def search(self, search):
        s = Search(search)
        id = re.split('videoId=', str(s.results[0]))[1]

        link = f'https://www.youtube.com/watch?v={id}'
        video = YouTube(link)

        title = video.title

        print(f'Title:{title}, link:{link}')

        regex = '[/\:?*|"]'
        title = re.sub(regex, "", title)

        return title, link

    def download(self, link, title):
        video = YouTube(link)
        streams = video.streams.filter(only_audio=True, bitrate="128kbps")
        streams[0].download(filename=f"{title}.mp3")

class Client(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.audio = Audio(bot)

    #@commands.command(name='init')
    #async def init(self, ctx):
    #    self.audio = Audio(bot, ctx)
    #    print('Initialized')

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, search):
        title, link = self.audio.search(search)
        self.audio.add_to_queue(title, ctx)
        self.audio.download(link, title)


        await ctx.send(search)



bot = commands.Bot(command_prefix='!')
bot.add_cog(Client(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} connected')


bot.run(os.getenv('TOKEN'))
