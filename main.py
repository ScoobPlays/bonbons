import discord #imports
import os
import platform
import random
from PIL import Image
from discord.ext import commands
from datetime import datetime
from server import server

token = os.environ['token']
bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'),case_insensitive=True, intents = discord.Intents.all())
bot.remove_command("help")
bot.launch_time = datetime.utcnow() #variables & etc

@bot.event
async def on_ready(): #events
  print(f'Bot is ready to be used! Ping: {round(bot.latency * 1000)}')
  await bot.change_presence(status=discord.Status.dnd)

  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(aliases=['ping', 'uptime'], hidden=True) #stats command for ping & uptime
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

@bot.command(aliases=['hex', 'colour'])
async def color(ctx, inputcolor=''):
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
              await ctx.send(embed=embed)
              return
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
          return

server() #server function
os.environ.setdefault('JISHAKU_NO_UNDERSCORE', '1') #Jishaku envs
os.environ.setdefault('JISHAKU_HIDE', '1')
bot.load_extension('jishaku')

bot.run(token) #running the bot
