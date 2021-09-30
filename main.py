import discord 
import os
from discord.ext import commands
from datetime import datetime
from keep_alive import keep_alive

# gold = #fff1b6
# light_blue = #96daff

token = os.environ['token']
bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), case_insensitive=True, intents = discord.Intents.all(), allowed_mentions=discord.AllowedMentions(everyone=False))

@bot.event
async def on_ready():
  print(f'Bot is ready to be used! Ping: {round(bot.latency * 1000)}')
  await bot.change_presence(status=discord.Status.dnd)

  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
      destination = self.get_destination()
      for page in self.paginator.pages:
        embed = discord.Embed(description=page)
        await destination.send(embed=embed)
    
    async def send_command_help(self, command):
      embed = discord.Embed(title=self.get_command_signature(command))
      embed.add_field(name="Help", value=command.help)
      command_has_alias = command.aliases
      command_has_help = command.help
      if command_has_help:
        embed.add_field(name="Help", value=command.help)
      if command_has_alias:
        embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)

      channel = self.get_destination()
      await channel.send(embed=embed)
    
    async def send_error_message(self, error):
      embed = discord.Embed(title="Error", description=error)
      channel = self.get_destination()
      await channel.send(embed=embed)

bot.help_command = MyNewHelp()
keep_alive()
os.environ.setdefault('JISHAKU_NO_UNDERSCORE', '1')
os.environ.setdefault('JISHAKU_HIDE', '1')
bot.load_extension('jishaku')
bot.run(token)
