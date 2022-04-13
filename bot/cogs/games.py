import discord
from discord.ext.commands import Cog, Context, command
from utils.bot import Bonbons


class Games(Cog):
    """
    Games to play around with.
    """

    def __init__(self, bot: Bonbons) -> None:
        self.bot = bot

    @property
    def emoji(self) -> str:
        return "🎮"

async def setup(bot: Bonbons):
    print("Loaded: Games")
    await bot.add_cog(Games(bot))
