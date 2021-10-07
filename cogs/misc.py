from discord.ext import commands
import random
import discord
from PIL import Image
from datetime import datetime
import base64
import asyncio
import requests

class Misc(commands.Cog):

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

    @commands.command()
    async def thank(self, ctx, member: commands.MemberConverter=None, *, reason=None):

      if member is None:
        embed=discord.Embed(description='Please mention a user to thank.', color=discord.Color.red())
        return await ctx.send(embed=embed)

      if reason is None:
        embed=discord.Embed(description='Please add a reason.', color=discord.Color.red())
        return await ctx.send(embed=embed)

      embed=discord.Embed(description=f'You thanked {member.mention}!', color=discord.Color.green())
      await ctx.send(embed=embed)

    @commands.command()
    async def endgame(self, ctx):
      await ctx.send("https://www.youtube.com/watch?v=dE1P4zDhhqw")

    @commands.command()
    async def encode(self, ctx, *, text):
      message_bytes = text.encode('ascii')
      base64_bytes = base64.b64encode(message_bytes)
      base64_message = base64_bytes.decode('ascii')
      embed=discord.Embed(title='✅ Message Was Encoded', color=discord.Color.green())
      embed.add_field(name='Output:', value=base64_message)
      await ctx.send(embed=embed)

    @encode.error
    async def encode_error(self, ctx, error):
      embed=discord.Embed(
        title="Encoding Error",
        description="Sorry, I couldn't encode that message."
        )
      await ctx.send(embed=embed)

    @commands.command()
    async def decode(self, ctx, *, text):
      base64_bytes = text.encode('ascii')
      message_bytes = base64.b64decode(base64_bytes)
      message = message_bytes.decode('ascii')
      embed=discord.Embed(title='✅ Message Was Encoded', color=discord.Color.green())
      embed.add_field(name='Output:', value=message)
      await ctx.send(embed=embed)

    @decode.error
    async def decode_error(self, ctx, error):
      embed=discord.Embed(
        title="Decoding Error",
        description="Sorry, I couldn't decode that message."
        )
      await ctx.send(embed=embed)

    @commands.command(aliases=['s'], help='Says whatever you want for you!')
    async def say(self, ctx, *, message):
      embed=discord.Embed(description = f'{message}', color=ctx.author.color)
      embed.set_author(name=f'{ctx.author.name}', icon_url = ctx.author.display_avatar)
      embed.timestamp = datetime.utcnow()
      await ctx.send(embed=embed)

    @commands.command(description='Says whatever you want using a webhook.')
    async def echo(self, ctx, *, message):

      webhook = await ctx.channel.create_webhook(
        name=ctx.author.name
        )
      #await ctx.message.delete()
      await webhook.send(message)
      await webhook.delete()
      await ctx.message.delete()

    @echo.error
    async def echo_error(self, ctx, error):
      embed=discord.Embed(
        title="Error",
        description="Sorry, I couldn't echo that message."
        )
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))