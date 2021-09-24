from discord.ext import commands
import os
import discord
import sys
import random
from jishaku.codeblocks import codeblock_converter

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

class Owner(commands.Cog):
    def __init__(self, client):
      self.client = client
  
    @commands.command(aliases=['eval', 'run'])
    async def _eval(self, ctx, *, code: codeblock_converter):
      cog = self.client.get_cog("Jishaku")
      await cog.jsk_python(ctx, argument=code)

    @commands.command(aliases=['rs'], hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
      await ctx.message.delete()
      embed=discord.Embed(title='Restarting 🕛', description=f'Approximate time to restart is `{random.randint(2, 5)}.{random.randint(2, 9)}` seconds.')
      await ctx.send(embed=embed)
      print('Restarting...')
      restart_bot()
      
def setup(client):
  client.add_cog(Owner(client))