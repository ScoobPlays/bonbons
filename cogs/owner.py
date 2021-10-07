from discord.ext import commands
import os
import discord
import sys

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

class Owner(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
  
    @commands.command(aliases=['rs', 'shutdown'])
    async def restart(self, ctx):
      embed=discord.Embed(title='Restarting...', color=discord.Color.red())
      await ctx.send(embed=embed)
      print('Restarting...')
      restart_bot()

def setup(bot):
  bot.add_cog(Owner(bot))