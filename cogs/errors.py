import discord
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
        description=f"> {error}",
        color=discord.Color.red()
        )
      await ctx.send(embed=embed, delete_after=10)


    elif isinstance(error, commands.CommandOnCooldown): #cd error
      print(error)
      embed=discord.Embed(
        title='Command On Cooldown', 
        description=f"> Command is on cooldown. Try again in **{error.retry_after}** seconds.",
        color=discord.Color.red()
        )
      await ctx.send(embed=embed, delete_after=10)


    elif isinstance(error, commands.MissingRequiredArgument): #missing arg
      print(error)
      embed=discord.Embed(
        title='Missing Required Argument',
        description=f"> {error}",
        color=discord.Color.red()
        )
      await ctx.send(embed=embed, delete_after=10)

    else: #unknown error
      stdout = io.StringIO()
      value = stdout.getvalue()

      embed=discord.Embed(
        title='Error', 
        color=discord.Color.red()
        )
      embed.add_field(name='Error', value=f"```{error}```", inline=False)
      if ctx.author is ctx.guild.owner:
        embed.add_field(name='Console',value=f'```py\n{value}{traceback.format_exc()}\n```', inline=False)
      await ctx.send(embed=embed, delete_after=10)

def setup(bot):
  bot.add_cog(Errors(bot))
