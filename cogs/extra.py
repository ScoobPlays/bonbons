import discord
from discord.ext import commands
import requests
import json
from datetime import datetime
import base64
import random
import aiohttp

class Extra(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
  
  @commands.command(aliases=['wiki'])
  async def wikipedia(self, ctx, *, query: str):
    sea = requests.get(
        ('https://en.wikipedia.org//w/api.php?action=query'
         '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
        ).format(query)).json()['query']

    if sea['searchinfo']['totalhits'] == 0:
        await ctx.send('Sorry, your search could not be found.')
    else:
        for x in range(len(sea['search'])):
            article = sea['search'][x]['title']
            req = requests.get('https://en.wikipedia.org//w/api.php?action=query'
                               '&utf8=1&redirects&format=json&prop=info|images'
                               '&inprop=url&titles={}'.format(article)).json()['query']['pages']
            if str(list(req)[0]) != "-1":
                break
        else:
            await ctx.send('Sorry, your search could not be found.')
            return
        article = req[list(req)[0]]['title']
        arturl = req[list(req)[0]]['fullurl']
        artdesc = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+article).json()['extract']
        embed = discord.Embed(title='**'+article+'**', url=arturl, description=artdesc, color=0x3FCAFF)
        embed.set_footer(text=f'Search result for {query}',
                         icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
        embed.set_author(name='Wikipedia', url='https://en.wikipedia.org/',
                         icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

  @commands.command(aliases=['skin', 'mc'])
  async def minecraft(self, ctx, username='Shrek'):

    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'
                        .format(username)).json()['id']

    url = json.loads(base64.b64decode(requests.get(
        'https://sessionserver.mojang.com/session/minecraft/profile/{}'
        .format(uuid)).json()['properties'][0]['value'])
                     .decode('utf-8'))['textures']['SKIN']['url']
    
    names = requests.get('https://api.mojang.com/user/profiles/{}/names'
                        .format(uuid)).json()
    history = ""
    for name in reversed(names):
        history += name['name']+"\n"

    embed=discord.Embed(title=f'User Information For {username}')
    embed.add_field(name='Username', value=username)
    embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
    embed.add_field(name='History', value=history)
    embed.set_thumbnail(url=url)
    embed.set_footer(icon_url=ctx.author.display_avatar)
    embed.timestamp=datetime.utcnow()
    await ctx.send(embed=embed)

  @commands.command(help='Kisses a user! :flushed:')
  async def kiss(self, ctx, member: commands.MemberConverter):
    await ctx.send(f"{ctx.author.mention} kissed {member.mention}!!\nhttps://tenor.com/view/milk-and-mocha-bear-couple-kisses-kiss-love-gif-12498627")


  @commands.command(help='Bonks a user!')
  async def bonk(self, ctx, member: commands.MemberConverter):
    bonkis = ['https://tenor.com/view/despicable-me-minions-bonk-hitting-cute-gif-17663380', 'https://tenor.com/view/lol-gif-21667170', 'https://tenor.com/view/azura-bonk-azura-bonk-gif-21733152']
    bonkiuwu = random.choice(bonkis)
    await ctx.send(f"{ctx.author.mention} bonked {member.mention}!\n{bonkiuwu}")

  @commands.command(help='Spanks a user! :flushed:')
  async def spank(self, ctx, member: commands.MemberConverter):
    await ctx.send(f'{ctx.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590')

  @commands.command(help='Slaps a user!')
  async def slap(self, ctx, member: commands.MemberConverter):  
    await ctx.send(f'{ctx.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299')

  @commands.command(help='Winks at a user!')
  async def wink(self, ctx, member: commands.MemberConverter):
    async with aiohttp.ClientSession() as cs:
      async with cs.get("https://some-random-api.ml/animu/wink") as r:
        data = await r.json()
        image = data["link"]
        await ctx.send(f'{ctx.author.mention} winked at {member.mention}!!\n{image}')
     
  @commands.command(help='Pats a user!')
  async def pat(self, ctx, member: commands.MemberConverter):
    async with aiohttp.ClientSession() as cs:
      async with cs.get("https://some-random-api.ml/animu/pat") as r:
        data = await r.json()
        image = data["link"]
        await ctx.send(f"{ctx.author.mention} patted {member.mention}!!\n{image}")

  @commands.command(help='Hugs a user.')
  async def hug(self, ctx, member: commands.MemberConverter):
    async with aiohttp.ClientSession() as cs:
      async with cs.get("https://some-random-api.ml/animu/hug") as r:
        data = await r.json()
        image = data["link"]
        await ctx.send(f'{ctx.author.mention} hugged {member.mention}!!\n{image}')

def setup(bot):
  bot.add_cog(Extra(bot))
