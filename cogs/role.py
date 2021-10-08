import discord
from discord.ext import commands
from datetime import datetime

prefix = "."

class Roles(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, roles):

      github_role = ctx.guild.get_role(895210078133710929)
      
      if roles == "github":

        if github_role in ctx.author.roles:

          await ctx.author.remove_roles(github_role)

          embed=discord.Embed(
            description='Removed the **github** role!'
            )

          embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
          embed.timestamp=datetime.utcnow()
          await ctx.send(embed=embed)
          return
        
        await ctx.author.add_roles(github_role)

        embed=discord.Embed(
          description='Gave you the **github** role!'
          )

        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.timestamp=datetime.utcnow()
        await ctx.send(embed=embed)


    @role.error
    async def role_error(self, ctx, error):

      embed=discord.Embed(
        title='Error',
        description='Please type the role name correctly!'
      )
      embed.timestamp=datetime.utcnow()
      await ctx.send(embed=embed)
    
def setup(bot):
  bot.add_cog(Roles(bot))
