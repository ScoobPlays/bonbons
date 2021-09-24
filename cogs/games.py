from datetime import datetime
import discord
from discord.ext import commands
from discordTogether import DiscordTogether

class Games(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.togetherControl = DiscordTogether(client)

    @commands.command(name='fishing', help='Opens a Fishing game.')
    async def _fishing(self, ctx):
      try:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
        await ctx.send(f"{link}")
      except:
        await ctx.reply("You must be in a VC to use this command.")

    @commands.command(name='youtube', help='Opens a Youtube link!')
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

def setup(client):
  client.add_cog(Games(client)) 