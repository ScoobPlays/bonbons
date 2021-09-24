import aiohttp
import discord
import random
from aiohttp import ContentTypeError
from discord import Color, Embed
from discord.ext.commands import Cog, Context, command
import discord.utils
from discord.ext import commands
from datetime import datetime
import requests

class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
      r = requests.get(f"https://some-random-api.ml/meme").json()
      image_url = r["image"]
      em = discord.Embed(title=r["caption"])
      em.set_image(url=image_url)
      em.timestamp=datetime.utcnow()
      await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Reddit(bot))
