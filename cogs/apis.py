import discord
from discord.ext import commands
import requests
import json
from datetime import datetime
import base64

class APIs(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
  
  @commands.command(aliases=['wiki'])
  async def wikipedia(ctx, *, query: str):
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
  async def minecraft(ctx, username='Shrek'):

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

def setup(bot):
  bot.add_cog(APIs(bot))
