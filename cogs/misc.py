from discord.ext import commands
import random
import discord
from datetime import datetime
import aiohttp

class Miscellaneous(commands.Cog):

    def __init__(self, bot):
      self.bot = bot
    
    @commands.command(help='Ships you with a member!')
    async def ship(self, ctx, bride: discord.Member, groom: discord.Member):
      love = random.randint(0, 100)
      print(love)

      if love > 99:
        embed=discord.Embed(description=f'{bride.mention} and {groom.mention} should marry! :heart:')
        embed.timestamp=datetime.utcnow()  
        await ctx.send(embed=embed)
       
      elif love > 49:
        embed=discord.Embed(description=f'{bride.mention} and {groom.mention} are lovers! :heart:')
        embed.timestamp=datetime.utcnow()
        await ctx.send(embed=embed)
      
      elif love < 10:
        embed=discord.Embed(description=f'{bride.mention} and {groom.mention} cannot be lovers! :broken_heart:')
        embed.timestamp=datetime.utcnow()
        await ctx.send(embed=embed)
  
      else:
        embed=discord.Embed(description=f'I ship {bride.mention} and {groom.mention}!! :heart:')
        embed.timestamp=datetime.utcnow()   
        await ctx.send(embed=embed)

    @commands.command(help='Kisses a user! :flushed:')
    async def kiss(self, ctx, member: commands.MemberConverter):  
      embed=discord.Embed(title=f'{ctx.author.name} kissed {member.name}')
      embed.set_image(url='https://tenor.com/view/kiss2-gif-21770023')
      await ctx.send(embed=embed)


    @commands.command(help='Bonks a user!')
    async def bonk(self, ctx, member: commands.MemberConverter):

      bonkis = ['https://tenor.com/view/despicable-me-minions-bonk-hitting-cute-gif-17663380', 'https://tenor.com/view/lol-gif-21667170', 'https://tenor.com/view/azura-bonk-azura-bonk-gif-21733152']
      bonkiuwu = random.choice(bonkis)
      embed=discord.Embed(title=f'{ctx.author.name} bonked {member.name}')
      embed.set_image(url=bonkiuwu)
      await ctx.send(embed=embed)

    @commands.command(help='Spanks a user! :flushed:')
    async def spank(self, ctx, member: commands.MemberConverter):  
      await ctx.channel.send(f'{ctx.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590')

    @commands.command(help='Slaps a user!')
    async def slap(self, ctx, member: commands.MemberConverter):  
      await ctx.channel.send(f'{ctx.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299')

    @commands.command(help='Winks at a user!')
    async def wink(self, ctx, member: commands.MemberConverter):
      async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/animu/wink") as r:
          data = await r.json()
          emb = discord.Embed(title = f'{ctx.author.name} winked at {member.display_name}')
          emb.set_image(url=data["link"])
          await ctx.send(embed=emb)
     
    @commands.command(help='Pats a user!')
    async def pat(self, ctx, member: commands.MemberConverter):
      async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/animu/pat") as r:
          data = await r.json()
          emb = discord.Embed(title = f'{ctx.author.name} patted {member.display_name}')
          emb.set_image(url=data["link"])
          await ctx.send(embed=emb)

    @commands.command(help='Hugs a user.')
    async def hug(self, ctx, member: commands.MemberConverter):
      async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/animu/hug") as r:
          data = await r.json()
          emb = discord.Embed(title = f'{ctx.author.name} hugged {member.display_name}')
          emb.set_image(url=data["link"])
          await ctx.send(embed=emb)

    @commands.command()
    async def thank(self, ctx, member: commands.MemberConverter=None, *, reason=None):
      if member is None:
        embed=discord.Embed(description='Please mention a user to thank.')
        await ctx.send(embed=embed)
        pass
        return
      if reason is None:
        embed=discord.Embed(description='Please add a reason.')
        await ctx.send(embed=embed)
        pass
        return
      embed=discord.Embed(description=f'You thanked {member.mention}!')
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
