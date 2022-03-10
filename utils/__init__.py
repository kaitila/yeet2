from .audio import Audio
from .song_handler import Handler


class Utils():
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
    
    queue = []