import discord
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
      em.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar)
      em.timestamp=datetime.utcnow()
      await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Reddit(bot))
