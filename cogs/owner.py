from discord.ext import commands
import os
import discord
import sys
from jishaku.codeblocks import codeblock_converter

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

class Owner(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
  
    @commands.command(aliases=['eval', 'run'])
    async def evaluate(self, ctx, *, code: codeblock_converter):
      cog = self.bot.get_cog("Jishaku")
      await cog.jsk_python(ctx, argument=code)

    @commands.command(aliases=['rs', 'shut', 'shutdown', 'fuckoff'])
    async def restart(self, ctx):
      embed=discord.Embed(title='Restarting...', color=discord.Color.red())
      await ctx.send(embed=embed)
      print('Restarting...')
      restart_bot()
      
def setup(bot):
  bot.add_cog(Owner(bot))