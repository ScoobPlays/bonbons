from discord.ext import commands
import random
import discord
from datetime import datetime
import base64
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
        embed=discord.Embed(description='Please mention a user to thank.', delete_after=5)
        return await ctx.send(embed=embed)

      if reason is None:
        embed=discord.Embed(description='Please add a reason.', delete_after=5)
        return await ctx.send(embed=embed)

      embed=discord.Embed(description=f'You thanked {member.mention}!')
      await ctx.send(embed=embed)

    @commands.command()
    async def endgame(self, ctx):
      await ctx.send("https://www.youtube.com/watch?v=dE1P4zDhhqw")

    @commands.command()
    async def encode(self, ctx, text):
      message_bytes = text.encode('ascii')
      base64_bytes = base64.b64encode(message_bytes)
      base64_message = base64_bytes.decode('ascii')
      embed=discord.Embed(title='✅ Message Was Encoded')
      embed.add_field(name='Output:', value=base64_message)
      await ctx.send(embed=embed)

    @commands.command()
    async def decode(self, ctx, text):
      base64_bytes = text.encode('ascii')
      message_bytes = base64.b64decode(base64_bytes)
      message = message_bytes.decode('ascii')
      embed=discord.Embed(title='✅ Message Was Encoded')
      embed.add_field(name='Output:', value=message)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
