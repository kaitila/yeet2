from utils import Utils


class Actions(Utils):
    def add_to_queue(self, title, ctx):
        """
        Adds {title} to {self.queue}

        """
        try: self.queue[ctx.guild.id]
        except KeyError: self.queue[ctx.guild.id] = []

        self.queue[ctx.guild.id].append(title)
        #print(self.queue)

    def get_queue(self):
        """
        Returns a message: str including all the items in {self.queue}

        """
        if self.queue[self.ctx.guild.id] == []: return '`Nothing in queue`'

        message = ''
        for i in range(0, len(self.queue[self.ctx.guild.id])):
                message += f'{i + 1}. {self.queue[self.ctx.guild.id][i]}\n'

        return message


