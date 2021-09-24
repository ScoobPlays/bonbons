import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['nickname', 'n'])
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: commands.MemberConverter=None, *, nick):
     
      if member == None:
        member = ctx.author

      try:
       await member.edit(nick=nick)
       embed=discord.Embed(description = f'You have changed {member.mention}\'s nick.', color=ctx.author.color)
       embed.set_author(name=f'{ctx.author.display_name}', icon_url = ctx.author.avatar.url)
       embed.timestamp = datetime.utcnow()
       await ctx.send(embed=embed)
     
      except: 
       embed=discord.Embed(description = f'I can\'t change {member.mention}\'s nick.', color=ctx.author.color)
       embed.set_author(name=f'{ctx.author.display_name}', icon_url = ctx.author.avatar.url)
       embed.timestamp = datetime.utcnow() 
       await ctx.send(embed=embed)

    @commands.command(aliases=['clear'], help='Purges an amount of messages.')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount:int = 2):
       await ctx.channel.purge(limit=amount)

    @commands.command(help='Adds/Removes a role from a member.')
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: commands.MemberConverter=None, *, role: commands.RoleConverter):

      if role in member.roles:
        await member.remove_roles(role)
        embed=discord.Embed(title='Role removed!', description=f'Removed {role.mention} from {member.mention}.')
        embed.timestamp=datetime.utcnow()
        await ctx.send(embed=embed)
      else:
        await member.add_roles(role)
        embed=discord.Embed(title='Role added!', description=f'Added {role.mention} to {member.mention}.')
        embed.timestamp=datetime.utcnow()
        await ctx.send(embed=embed)
    
    @commands.command(help="Mutes the specified user!")
    @commands.is_owner()
    async def mute(self,ctx, member: commands.MemberConverter, *, reason=None):
      guild = ctx.guild
      mutedRole = discord.utils.get(guild.roles, name="Redacted | Muted")
      
      if not mutedRole:
        mutedRole = await guild.create_role(name="Redacted | Muted")
      for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        
      await member.add_roles(mutedRole, reason=reason)
      await ctx.send(f"Muted {member.name}#{member.discriminator}.")
      await member.send(f"You were muted in the server **{guild.name}** for **{reason}**")

    @commands.command(help="Unmutes a user.")
    @commands.is_owner()
    async def unmute(self, ctx, member: commands.MemberConverter):
      mutedRole = discord.utils.get(ctx.guild.roles, name="Redacted | Muted")
      await member.remove_roles(mutedRole)
      await ctx.send(f"Unmuted {member.name}#{member.discriminator}.")
      
    @commands.command(help="Bans a member.")
    @commands.is_owner()
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
      await member.ban(reason=reason)
      await ctx.send(f"{member.name}#{member.discriminator} was banned.")	
      
    @commands.command(help="Unbans a member.")
    @commands.is_owner()
    async def unban(self, ctx, *, member):
      bannedUsers = await ctx.guild.bans()
      name, discriminator = member.split("#")
      
      for ban in bannedUsers:
        user = ban.user
        
        if(user.name, user.discriminator) == (name, discriminator):
          await ctx.guild.unban(user)
          await ctx.send(f"{user.name}#{user.discriminator} was unbanned.")
          return	

def setup(bot):
   bot.add_cog(Moderation(bot))
