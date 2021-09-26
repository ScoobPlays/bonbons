import discord #imports
import os
import platform
import random
from discord.ext import commands
from datetime import datetime
from keep_alive import keep_alive

# gold = #fff1b6
# light_blue = #96daff


token = os.environ['token']
bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), case_insensitive=True, intents = discord.Intents.all())
bot.remove_command("help")
bot.launch_time = datetime.utcnow() #variables & etc

@bot.event
async def on_ready(): #events
  print(f'Bot is ready to be used! Ping: {round(bot.latency * 1000)}')
  await bot.change_presence(status=discord.Status.dnd)

  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(aliases=['ping', 'uptime']) #stats command for ping & uptime
async def stats(ctx):

  delta_uptime = datetime.utcnow() - bot.launch_time
  hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)

  embed=discord.Embed(title='Bot Statistics')
  embed.add_field(name='Uptime/Latency', value=f'`{hours}h, {minutes}m, {seconds}s` `{round(bot.latency * 1000)}ms`', inline=False)
  embed.add_field(name='Python', value=f"`{platform.python_version()}`")
  embed.add_field(name='Module', value=f"`Py-Cord 2.0`")
  embed.timestamp = datetime.utcnow()
  await ctx.send(embed=embed)

keep_alive() #Keep alive method for replit ^^
os.environ.setdefault('JISHAKU_NO_UNDERSCORE', '1') #Jishaku envs
os.environ.setdefault('JISHAKU_HIDE', '1')
bot.load_extension('jishaku')

bot.run(token) #running the bot
