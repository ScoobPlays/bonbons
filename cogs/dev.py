from disnake.ext import commands


class Development(commands.Cog, description="Commands that are a work in progress."):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Development(bot))
