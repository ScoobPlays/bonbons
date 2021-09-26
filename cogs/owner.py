from discord.ext import commands
import os
import discord
import sys
import random
from jishaku.codeblocks import codeblock_converter

list = ["y u click", "imagine clicking", "ok", "owo", "uwu", "OWOWOWOOW", "y u click.. d- do you like me? :flushed:"]
sano = random.choice(list)

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

class Owner(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
  
    @commands.command(aliases=['eval', 'run'])
    async def _eval(self, ctx, *, code: codeblock_converter):
      cog = self.bot.get_cog("Jishaku")
      await cog.jsk_python(ctx, argument=code)

    @commands.command(aliases=['rs'], hidden=True)
    async def restart(self, ctx):
      embed=discord.Embed(title='Restarting 🕛', description=f'||{sano}||')
      await ctx.send(embed=embed)
      print('Restarting...')
      restart_bot()
      
def setup(bot):
  bot.add_cog(Owner(bot))
