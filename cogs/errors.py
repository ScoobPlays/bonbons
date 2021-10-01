import discord
from datetime import datetime
from discord.ext import commands
import io
import traceback

class Errors(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    
    if hasattr(ctx.command, 'on_error'):
      return

    if isinstance(error, commands.DisabledCommand):
      print(error)
      embed=discord.Embed(
        title='Command Is Disabled', 
        url=ctx.message.jump_url,
        description=f"> {error}",
        color=discord.Color.red()
        )
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    elif isinstance(error, commands.CommandOnCooldown): #cd error
      print(error)
      embed=discord.Embed(
        title='Command On Cooldown', 
        url=ctx.message.jump_url,
        description=f"> Command is on cooldown. Try again in **{error.retry_after}** seconds.",
        color=discord.Color.red()
        )
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    elif isinstance(error, commands.MissingRequiredArgument): #missing arg
      print(error)
      embed=discord.Embed(
        title='Missing Required Argument',
        url=ctx.message.jump_url, 
        description=f"> {error}",
        color=discord.Color.red()
        )
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    elif isinstance(error, commands.NotOwner): #owner only error
      print(error)
      embed=discord.Embed(
        title='Not Owner',
        url=ctx.message.jump_url,
        description=f"> {error}",
        color=discord.Color.red()
        )
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)


    else: #unknown error
      print(error)
      stdout = io.StringIO()
      value = stdout.getvalue()

      embed=discord.Embed(
        title='Unknown/Unregistered Error', 
        url=ctx.message.jump_url, 
        description=f"> **Error:** {error}\n> **Name:** {ctx.command or None}\n> **Cog:** {ctx.cog}",
        color=discord.Color.red()
        )
      embed.add_field(name='Console',value=f'```py\n{value}{traceback.format_exc()}\n```')
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Errors(bot))
