from datetime import datetime
import discord
from discord.ext import commands
import random
import aiohttp
from discordTogether import DiscordTogether


class Fun(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.last_msg = None
        self.togetherControl = DiscordTogether(bot)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message): #on msg delete for snipe command
      self.last_msg = message

    @commands.command(help='Snipes the most recently deleted message.')
    async def snipe(self, ctx):
      embed = discord.Embed(description=f"{self.last_msg.content}")
      embed.set_footer(text=f"Message from {self.last_msg.author}")
      embed.set_author(name=f'{self.last_msg.author}', icon_url=self.last_msg.author.display_avatar)
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)

    @snipe.error
    async def snipe_error(self, ctx, error):

      embed=discord.Embed(
        title='Error',
        description='Sorry, I couldn\'t find the most recently deleted message or the deleted message was an Image, Embed or File.'
      )

      embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
      embed.set_timestamp=datetime.utcnow()
      await ctx.send(embed=embed)

    @commands.command()
    async def luck(self, ctx, *, lucky_on):
      randome=random.randint(0, 100)

      random_day = ['tomorrow is', 'next week is', 'this Friday is', 'this Monday is', 'next year is', 'in 2050 is']
      rng_day = random.choice(random_day)

      embed=discord.Embed(description=f'Your luck of getting **{lucky_on}** {rng_day} **{randome}**%', color=ctx.author.color)
      embed.set_timestamp=datetime.utcnow()
      await ctx.send(embed=embed)

    @commands.command(help='Generates a random token.')
    async def token(self, ctx):
      async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/bottoken") as r:
          data = await r.json()
          
          emb = discord.Embed(description=data["token"])
          emb.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=f'{ctx.author.display_avatar}')
          emb.timestamp=datetime.utcnow()
          await ctx.send(embed=emb)

    @commands.command(help='Gives a joke!')
    async def joke(self, ctx):
      async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://some-random-api.ml/joke") as r:
          data = await r.json()
          await ctx.send(data['joke'])

    @commands.command(aliases=['roll'])
    async def dice(self, ctx):
      await ctx.send(f"You rolled a {random.randint(1, 6)}!")

    @commands.command(name='fishing', help='Opens a Fishing game.')
    async def _fishing(self, ctx):
      try:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
        await ctx.send(f"{link}")
      except:
        await ctx.reply("You must be in a VC to use this command.")

    @commands.command(name='youtube', help='Starts a Youtube activity.')
    async def _youtube(self, ctx):
      try:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"{link}")
      except:
        await ctx.reply("You must be in a VC to use this command.")

    @commands.command(name='poker', help='Opens a Poker game.')
    async def _poker(self, ctx):
      try:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'poker')
        await ctx.send(f"{link}")
      except:
        await ctx.reply("You must be in a VC to use this command.")

    @commands.command(name='betrayal', help='Opens a Betrayal game.')
    async def _betrayal(self, ctx):
      try:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal')
        await ctx.send(f"{link}")
        
      except:
        await ctx.reply("You must be in a VC to use this command.")
    
    @commands.command(name='chess', help='Opens a Chess game.')
    async def _chess(self, ctx):
      try:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'poker')
        await ctx.send(f"{link}")
      except:
        await ctx.reply("You must be in a VC to use this command.")

def setup(bot):
  bot.add_cog(Fun(bot))
