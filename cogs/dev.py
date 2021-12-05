from disnake.ext import commands
from utils.env import cluster
import disnake

class Development(commands.Cog, description="Commands that are a work in progress."):
    def __init__(self, bot):
        self.bot = bot
        self.afk = cluster["afk"]

    @property
    def cmds(self):
        command = self.bot.cogs["Development"].get_commands()
        return command

def setup(bot):
    bot.add_cog(Development(bot))
