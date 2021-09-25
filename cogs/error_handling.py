import discord
from discord.ext import commands

class Errors(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound): #command not found
      embed=discord.Embed(title='Command Not Found',url=ctx.message.jump_url, description=error)
      await ctx.send(embed=embed)
      
    if isinstance(error, commands.DisabledCommand): #disabled command
      embed=discord.Embed(title='Command Is Disabled', url=ctx.message.jump_url,description=error)
      await ctx.send(embed=embed)
      
    elif isinstance(error, commands.CommandOnCooldown): #cd error
      embed=discord.Embed(title='Command On Cooldown', url=ctx.message.jump_url,description=f"Command is on cooldown. Try again in **{error.retry_after}** seconds.")
      await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument): #missing arg
      embed=discord.Embed(title='Missing Required Argument', url=ctx.message.jump_url,description=error)
      await ctx.send(embed=embed)

    elif isinstance(error, commands.TooManyArguments): #too many args
      embed=discord.Embed(title='Too Many Arguments', url=ctx.message.jump_url,description=error)
      await ctx.send(embed=embed)

    elif isinstance(error, commands.NotOwner): #owner only error
      embed=discord.Embed(title='Owner Command', url=ctx.message.jump_url,description=error)
      await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound): #member not found
      embed=discord.Embed(title='Member Not Found', url=ctx.message.jump_url,description=error)
      await ctx.send(embed=embed)

    elif isinstance(error, commands.GuildNotFound): #server not found
      embed=discord.Embed(title='Guild Not found',url=ctx.message.jump_url, description=error)
      await ctx.send(embed=embed)

    else: #unknown error
      embed=discord.Embed(title='Unknown/Unregistered Error', url=ctx.message.jump_url, description=f"Error: {error}\nName: {ctx.command.name}\nCog: {ctx.cog}")
      await ctx.send(embed=embed)
      

def setup(bot):
  bot.add_cog(Errors(bot))
