from pytube import YouTube
from pytube import Search

from utils import Utils

import re
import os


class Handler(Utils):
    def search(self, search):
        """
        Performes a YouTube search of {search}
        returns the link and title of the first result

        """
        yt_search = Search(search)
        id = re.split('videoId=', str(yt_search.results[0]))[1]

        link = f'https://www.youtube.com/watch?v={id}'
        video = YouTube(link)

        title = video.title
        regex = '[/\:?*|"]'
        title = re.sub(regex, "", title)

        return title, link

    def download(self, link, title):
        """
        Downloads audio from {link}
        stores it in {title}.mp3

        """
        video = YouTube(link)
        streams = video.streams.filter(only_audio=True, bitrate="128kbps")
        streams[0].download(filename=f"{title}.mp3")

    #Return a search from song library \songs
    def lib_search(self, search):
        """
        Performes a search in the local song library /songs for matching keywords
        returns the title of the best match
        
        """
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