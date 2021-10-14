import discord
from discord.ext import commands
import os
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
    @commands.is_owner()
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

    @commands.command()
    async def help(self, ctx):
      embed=discord.Embed(
        title='Help Page',
        color=discord.Color.green()
        )
      embed.add_field(name='Main', value="`kiss`, `bonk`, `spank`, `slap`, `wink`, `pat`, `hug`")
      embed.add_field(name='Misc', value="`say`, `luck`, `encode`, `decode`, `wiki`, `mincraft`, `dog`, `cat`, `snipe`, `color`, `token`, `joke`")
      embed.add_field(name='Information', value="`membercount`, `userinfo`, `serverinfo`, `roleinfo`, `spotify`, `avatar`")
      embed.add_field(name='Utility', value="`ping`, `nick`, `massnick`, `ban`, `unban`, `clean`")
      embed.add_field(name='Other', value="`stats`, `run`, `jsk`, `restart`")
      embed.timestamp=datetime.utcnow()
      embed.set_footer(text=f"Commands: {len(self.bot.commands)}", icon_url=ctx.author.display_avatar)
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Owner(bot))
