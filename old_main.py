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


#Handles audio actions
class Audio():
    def __init__(self, bot, ctx):
        self.bot = bot
        self.audio_player = bot.loop.create_task(self.audio_player())
        self.queue = []
        self.ctx = ctx

    #Automatically plays audio from the queue
    async def audio_player(self):
        while True:
            await asyncio.sleep(1)
            if len(self.queue) > 0:
                try:
                    await self.ctx.author.voice.channel.connect()
                    #self.voice = discord.utils.get(self.bot.voice_clients, guild=self.ctx.guild)
                except: pass

                self.voice = discord.utils.get(self.bot.voice_clients, guild=self.ctx.guild)

                if not self.voice.is_playing():
                    self.voice.play(discord.FFmpegPCMAudio(f"{self.queue[0]}.mp3"))
                    await self.ctx.send(f'`Now playing: {self.queue[0]}`')
                    self.queue.pop()


        
    def add_to_queue(self, title, ctx):
        #try: self.queue[ctx.guild.id]
        #except KeyError: self.queue[ctx.guild.id] = []

        self.queue.append(title)
        print(self.queue)     

    def search(self, search):
        yt_search = Search(search)
        id = re.split('videoId=', str(yt_search.results[0]))[1]

        link = f'https://www.youtube.com/watch?v={id}'
        video = YouTube(link)

        title = video.title
        regex = '[/\:?*|"]'
        title = re.sub(regex, "", title)

        return title, link

    def download(self, link, title):
        video = YouTube(link)
        streams = video.streams.filter(only_audio=True, bitrate="128kbps")
        streams[0].download(filename=f"{title}.mp3")

    #Return a search from song library \songs
    def lib_search(self, search):
        search = search.lower()
        result = [0, ""]

        for song in os.listdir():
            #Get filename and check for matching words
            matches = re.findall(search, str(re.sub(".mp3", "", song)).lower())

            if len(matches) > result[0]:
                result = [len(matches), str(re.sub(".mp3", "", song))]
            elif len(matches) == result[0] and len(str(re.sub(".mp3", "", song))) < len(result[1]):
                result = [len(matches), str(re.sub(".mp3", "", song))]

        if result[1] == '': return False
        return result[1]

    def skip(self):
        try:
            self.voice.stop()
            return '`Skipping the current song!`'
        except:
            return '`Nothing is playing!`'

    def get_queue(self):
        if self.queue == []: return '`Nothing in queue`'

        message = ''
        for i in range(0, len(self.queue)):
            message += f'{i + 1}. {self.queue[i]}\n'
        
        return message


#Main command handler
class Client(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.init = False
        #self.audio = Audio(bot)

    #Executes before every command
    async def cog_before_invoke(self, ctx):
        if not self.init:
            self.audio = Audio(bot, ctx)
            self.init = True
            print(f'Initialized Audio() in {ctx.guild}')

        #Updates commands.Context in Audio()
        self.audio.ctx = ctx

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, search):
        if not self.audio.lib_search(search):
            await ctx.send('`No matches in the song library!`')
            title, link = self.audio.search(search)
            await ctx.send(f'`Downloading: {title}`')
            self.audio.download(link, title)
        else:
            title = self.audio.lib_search(search)
        
        self.audio.add_to_queue(title, ctx)
        await ctx.send(f'`Added to the queue: {title}`')

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        await ctx.send(self.audio.skip())

    @commands.command(name='leave')
    async def leave(self, ctx):
        await self.audio.voice.disconnect()

    @commands.command(name='queue')
    async def queue(self, ctx):
        await ctx.send(self.audio.get_queue())


bot = commands.Bot(command_prefix='!')
bot.add_cog(Client(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} connected')


bot.run(os.getenv('TOKEN'))
