from discord.ext import commands
import random
import discord
from PIL import Image
from datetime import datetime
import base64
import requests

class Miscellaneous(commands.Cog):

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
        embed=discord.Embed(description='Please mention a user to thank.')
        return await ctx.send(embed=embed)

      if reason is None:
        embed=discord.Embed(description='Please add a reason.')
        return await ctx.send(embed=embed)

      embed=discord.Embed(description=f'You thanked {member.mention}!')
      await ctx.send(embed=embed)

    @commands.command()
    async def endgame(self, ctx):
      await ctx.send("https://www.youtube.com/watch?v=dE1P4zDhhqw")

    @commands.command(aliases=['hex', 'colour'])
    async def color(self, ctx, inputcolor=''):
      
      if inputcolor == '':
        
        randgb = lambda: random.randint(0, 255)
        hexcode = '%02X%02X%02X' % (randgb(), randgb(), randgb())
        rgbcode = str(tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4)))
        heximg = Image.new("RGB", (256, 256), '#' + hexcode)
        heximg.save("color.png")
        f = discord.File("color.png", filename="color.png")
        embed=discord.Embed(title='Color Machine', color=discord.Color.random())
        embed.set_thumbnail(url="attachment://color.png")
        embed.add_field(name='RGB', value=f'`{rgbcode}`', inline=False)
        embed.add_field(name='Hex', value=f'`#{hexcode}`', inline=False)
        embed.timestamp=datetime.utcnow()
        await ctx.send(file=f, embed=embed)
        
      else:
        if inputcolor.startswith('#'):
          hexcode = inputcolor[1:]
          if len(hexcode) == 8:
            hexcode = hexcode[:-2]
          elif len(hexcode) != 6:
            embed=discord.Embed(description='Make sure you entered the correct code or format. `(#7289DA)`', color=ctx.author.color)
            return await ctx.send(embed=embed)
        
          rgbcode = str(tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4)))
          heximg = Image.new("RGB", (64, 64), '#' + hexcode)
          heximg.save("color.png")
          embed=discord.Embed(title='Color Machine', color=discord.Color.random())
          embed.set_thumbnail(url="attachment://color.png")
          f = discord.File("color.png", filename="color.png")
          embed.add_field(name='RGB', value=f'`{rgbcode}`', inline=False)
          embed.add_field(name='Hex', value=f'`#{hexcode}`', inline=False)
          embed.timestamp=datetime.utcnow()
          await ctx.send(file=f, embed=embed)
        
        else:
          embed=discord.Embed(description='Make sure you entered the correct code or format. `(#7289DA)`', color=ctx.author.color)
          await ctx.send(embed=embed)

    @commands.command()
    async def encode(self, ctx, *, text):
      message_bytes = text.encode('ascii')
      base64_bytes = base64.b64encode(message_bytes)
      base64_message = base64_bytes.decode('ascii')
      embed=discord.Embed(title='✅ Message Was Encoded')
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
      embed=discord.Embed(title='✅ Message Was Encoded')
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
    async def echo(self, ctx, *, text):
      webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=ctx.author.avatar)
      await ctx.message.delete()
      await webhook.send(text)
      await webhook.delete()

    @echo.error
    async def echo_error(self, ctx, error):
      embed=discord.Embed(
        title="Error",
        description="Sorry, I couldn't echo that message."
        )
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
