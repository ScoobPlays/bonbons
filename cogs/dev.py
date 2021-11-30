from disnake.ext import commands
from utils.env import cluster

class Development(commands.Cog, description="Commands that are a work in progress."):
    def __init__(self, bot):
        self.bot = bot
        self.afk = cluster["afk"]

    @property
    def commands(self):
        cog = self.bot.cogs["Development"].get_commands()
        return cog

def setup(bot):
    bot.add_cog(Development(bot))