import discord
from discord.ext import commands
from datetime import datetime
from discord import Spotify

class Information(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member : commands.MemberConverter=None):

      if member == None:
        member = ctx.author

      embed=discord.Embed(color=ctx.author.color)
      embed.set_image(url=member.display_avatar)
      embed.timestamp = datetime.utcnow()
      await ctx.send(embed=embed)

    @commands.command(aliases=['server'], help='Fetches the server\'s stats.')
    @commands.guild_only()
    async def serverinfo(self, ctx):

      embed=discord.Embed(color=ctx.author.color)
      embed.set_author(name=f'{ctx.guild.name}', icon_url = ctx.guild.icon.url)
      embed.add_field(name=f'Server Created At', value=f'<t:{int(ctx.guild.created_at.timestamp())}:D> (<t:{int(ctx.guild.created_at.timestamp())}:R>)', inline=False)
      embed.add_field(name='Information', value=f"• Members: {str(ctx.guild.member_count)}\n• Channels: {len(ctx.guild.channels)}\n• Emojis: {len(ctx.guild.emojis)}\n• Region: {ctx.guild.region}")
      embed.add_field(name=f'Server Roles [{len(ctx.guild.roles)}]', value=f' '.join(r.mention for r in ctx.guild.roles[1:]), inline=False)
      embed.timestamp = datetime.utcnow()
      embed.set_footer(text=f'Server ID: {ctx.guild.id}')
      embed.set_thumbnail(url=ctx.guild.icon.url)
      await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def membercount(self, ctx):
      embed=discord.Embed(title=f'Members', description=f'{len(ctx.guild.members)}', color=discord.Color.green())
      embed.timestamp = datetime.utcnow()
      await ctx.send(embed=embed)

    @commands.command(aliases=["userinfo", "u", "ui"])
    async def whois(self, ctx, member: commands.MemberConverter=None):

      if member == None:
        member = ctx.author

      if len(member.roles) > 1:
        role_string = ', '.join([r.mention for r in member.roles][1:])
        
      embed = discord.Embed(description=f"{member.mention}", color=member.color)
      embed.set_thumbnail(url=member.display_avatar)
      embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.display_avatar}')
      embed.add_field(name="Account Created At", value=f'<t:{int(member.created_at.timestamp())}:D> (<t:{int(member.created_at.timestamp())}:R>)')
      embed.add_field(name="Joined Server At", value=f'<t:{int(member.joined_at.timestamp())}:D> (<t:{int(member.joined_at.timestamp())}:R>')
      embed.add_field(name="Roles [{}]\n \n".format(len(member.roles)-1), value=role_string, inline=False)
      embed.add_field(name=f'Is Bot', value=member.bot)
      embed.add_field(name=f'Status', value=f'{member.activity}')
      embed.set_footer(text=f'User ID: {member.id}')
      embed.timestamp = datetime.utcnow()
      await ctx.send(embed=embed)

    @commands.command(help='Fetches your spotify activity/status. (if you have one)')
    async def spotify(self, ctx, member: commands.MemberConverter=None):

      if member == None:
        member = ctx.author
      
      for activity in member.activities:
        if isinstance(activity, Spotify):
          embed = discord.Embed(title = f"{member.name}'s Spotify", color = ctx.author.color)
          embed.set_thumbnail(url=activity.album_cover_url)
          embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.display_avatar}')
          embed.add_field(name='Song', value=activity.title)         
          embed.add_field(name="Artist", value=activity.artist)
          embed.add_field(name="Album", value=activity.album, inline=False)
          embed.set_footer(text=f"Track ID: {activity.track_id}")
          embed.timestamp=datetime.utcnow()
          await ctx.send(embed=embed)


    @commands.command(help='Gives you info about a role.')
    @commands.guild_only()
    async def roleinfo(self, ctx, role: commands.RoleConverter=None):

      if role == None:
        role = ctx.author.top_role

      embed = discord.Embed(description=f"{role.mention}", color=role.color)
      embed.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=f'{ctx.author.display_avatar}')
      embed.add_field(name="Role Created At", value=f'<t:{int(role.created_at.timestamp())}:D>')
      embed.add_field(name='Color', value=f"{role.color}")
      embed.add_field(name='Members', value=f"{len(role.members)}")
      embed.add_field(name='Position', value=f"{str(role.position)}/{len(ctx.guild.roles)}")
      embed.add_field(name='Hoisted', value=f"{role.hoist}")
      embed.add_field(name='Mentionable', value=f"{role.mentionable}")
      embed.set_footer(text=f'Role ID: {role.id}')
      embed.timestamp = datetime.utcnow()
      await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):

      embed=discord.Embed(
        title='Ponged!',
        description=f'Ping: {round(self.bot.latency * 1000)}ms'
        )
        
      embed.timestamp = datetime.utcnow()
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
