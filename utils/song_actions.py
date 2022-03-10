from .parent import Globals, Utils


class Actions(Utils):
    def add_to_queue(self, title):
        """
        Adds {title} to {self.queue}

        """

        Globals.queue.append(title)
        #print(self.queue)

    def get_queue(self):
        """
        Returns a message: str including all the items in {self.queue}

        """
        if Globals.queue == []: return '`Nothing in queue`'

        message = '`'
        for i in range(0, len(Globals.queue)):
                message += f'{i + 1}. {Globals.queue[i]}\n'

        return message + '`'

    def skip(self):
        try:
            Globals.voice.stop()
            return '`Skipping the current song!`'
        except:
            return '`Nothing is playing!`'


