import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):

      self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
    
      await self.bot.wait_until_ready()
      
      guild = self.bot.get_guild(880030618275155998)
      member_role = guild.get_role(880030723908722729)
    
      channel = guild.get_channel(880387280576061450)

      roles = [member_role]

      await member.add_roles(*roles)
      await channel.send(embed=discord.Embed(title='Welcome!', description=f'{member.mention} joined! Hope you stay!!').set_footer(text=member, icon_url=member.display_avatar))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
    
      await self.bot.wait_until_ready()
      
      guild = self.bot.get_guild(880030618275155998)    
      channel = guild.get_channel(880387280576061450)


      await channel.send(embed=discord.Embed(title='Goodbye!', description=f'{member.mention} left.. :cry:').set_footer(text=member, icon_url=member.display_avatar))

def setup(bot):
  bot.add_cog(Events(bot))
