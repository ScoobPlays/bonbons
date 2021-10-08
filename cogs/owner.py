from discord.ext import commands
import os
import discord
import sys
from datetime import datetime
import platform

hm = datetime.utcnow()

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

    @commands.command()
    @commands.is_owner()
    async def stats(self, ctx):
      
      delta_uptime = datetime.utcnow() - hm
      hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
      minutes, seconds = divmod(remainder, 60)
      days, hours = divmod(hours, 24)

      embed=discord.Embed(title='Bot Information')
      embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/888309915620372491/ee8c4ed341cb7cb954eefc7f08b879ec.png?size=1024")
      embed.add_field(name='Statistics', value=f"• Ping: {round(self.bot.latency * 1000)}ms\n• Uptime: {hours}h, {minutes}m, {seconds}s\n• Servers: {len(self.bot.guilds)}\n• Users: {len(self.bot.users)}\n• PyVersion: {platform.python_version()}")
      embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
      embed.timestamp = datetime.utcnow()
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Owner(bot))
