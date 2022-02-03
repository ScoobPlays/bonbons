from disnake.ext.commands import Bot
from docs import cog


class MyCog(cog.Docs):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.items = (
            ("disnake", "https://disnake.readthedocs.io/en/latest/"),
            ("python", "https://docs.python.org/3/'),
            ("aiohttp", "https://aiohttp.readthedocs.io/en/stable/"),
            ("nextcord", "https://nextcord.readthedocs.io/en/latest/"),
            ("pycord", "https://docs.pycord.dev/en/master/")
        )


def setup(bot: Bot):
    bot.add_cog(MyCog(bot))
