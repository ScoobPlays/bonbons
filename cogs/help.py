import discord
from datetime import datetime
from discord.ext import commands

class MyNewHelp(commands.MinimalHelpCommand):
      async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
          embed = discord.Embed(description=page)
          embed.timestamp=datetime.utcnow()
          embed.set_author(name=self.context.author, icon_url=self.context.author.display_avatar)
          embed.set_footer(text='Minimal Help Command', icon_url=self.context.author.display_avatar)
          await destination.send(embed=embed)
    
      async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
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

class Help(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      self.bot.help_command = MyNewHelp()

def setup(bot):
  bot.add_cog(Help(bot))