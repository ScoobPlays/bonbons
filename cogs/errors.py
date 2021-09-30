import discord
from datetime import datetime
from discord.ext import commands

class Errors(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    
    if hasattr(ctx.command, 'on_error'):
      return


    if isinstance(error, commands.CommandNotFound): #command not found
      print(error)
      embed=discord.Embed(
        title='Command Not Found',
        url=ctx.message.jump_url,
        description=f"> {error}"
        )
      embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    if isinstance(error, commands.DisabledCommand):
      print(error)
      embed=discord.Embed(
        title='Command Is Disabled', 
        url=ctx.message.jump_url,
        description=f"> {error}"
        )
      embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    elif isinstance(error, commands.CommandOnCooldown): #cd error
      print(error)
      embed=discord.Embed(
        title='Command On Cooldown', 
        url=ctx.message.jump_url,
        description=f"> Command is on cooldown. Try again in **{error.retry_after}** seconds."
        )
      embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    elif isinstance(error, commands.MissingRequiredArgument): #missing arg
      print(error)
      embed=discord.Embed(
        title='Missing Required Argument',
        url=ctx.message.jump_url, 
        description=f"> {error}"
        )
      embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    elif isinstance(error, commands.NotOwner): #owner only error
      print(error)
      embed=discord.Embed(
        title='Not Owner',
        url=ctx.message.jump_url,
        description=f"> {error}"
        )
      embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    else: #unknown error
      print(error)
      embed=discord.Embed(
        title='Unknown/Unregistered Error', 
        url=ctx.message.jump_url, 
        description=f"> Error: {error}\n> Name: {ctx.command or None}\n> Cog: {ctx.cog}"
        )
      embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)
      
def setup(bot):
  bot.add_cog(Errors(bot))
