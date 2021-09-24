import discord
import DiscordUtils
from discord.ext import commands
from datetime import datetime
import humanize
from discord.ext.commands import BucketType

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.cooldown(1,20, BucketType.user) 
  async def help(self, ctx):
    info=discord.Embed(title='1# Information Module ℹ', description='```Information type/related commands!```')
    info.add_field(name='-Commands', value='```Avatar: Fetches a users avatar.\nServerinfo: Gives the current servers statistics.\nMembercount: Fetches the amount of members in a server.\nWhois: Fetches information about a user.\nSpotify: Fetches a users spotify activity/status.\nRoleinfo: Gives information about a role.```', inline=False)
    info.add_field(name='-Usage', value='```.avatar <user>\n.whois <user>\n.spotify <user>\n.roleinfo <role>```', inline=False)
    info.set_footer(text='Page 1/5')
    info.set_image(url="https://cdn.discordapp.com/attachments/880030618275156001/890808109948342282/info.png")
    info.timestamp=datetime.utcnow()

    mod=discord.Embed(title='2# Moderation Module 🛠️', description="```Moderation commands for bad people!```")
    mod.add_field(name='-Commands', value='```Nick: Renaming users.\nPurge: Purges messages.\nRole: Adds/Removes a role from a user.```', inline=False)
    mod.add_field(name='-Usage', value='``.nick <user>\n.purge <messages>\n.role <role> <user>\n.unban <name+discrim>```', inline=False)
    mod.set_image(url="https://cdn.discordapp.com/attachments/880030618275156001/890807802908524574/moderation.png")
    mod.set_footer(text='Page 2/5')
    mod.timestamp=datetime.utcnow()

    websites=discord.Embed(title="3# APIs️ 🌐", description="```Commands that use the internet!```")
    websites.add_field(name='-Commands', value='```Wikipedia: Searchs the wiki for a term.\nMinecraft: Fetches the users skin & name history```', inline=False)
    websites.add_field(name='-Usage', value='```.wikipedia <query>\n.minecraft <username>```', inline=False)
    websites.set_footer(text='Page 3/5')
    websites.set_image(url="https://cdn.discordapp.com/attachments/880030618275156001/890812218432684052/apis.png")
    websites.timestamp=datetime.utcnow()

    fun=discord.Embed(title="4# Fun/Extra 🤭", description="```Funny/Extra commands.. that make you laugh!! (I think)```")
    fun.add_field(name='-Commands', value='```Joke: Gives you a joke!\nLuck: A luck rating!\nSay: Says something for you!\nSnipe: Snipes the most recently deleted message!\nColor: Generates a random hexcode or sends a hexcode if their was an input.\nToken: Grabs a random token! (Legit)\nYoutube: Opens a 3rd party Youtube link!\nFishing: Opens a Fishing game for you!\nPoker: Grabs an invite from the club! :eyes:\nBetrayal: Opens a game of Betrayal!\nChess: Opens a 3rd party Chess game!```', inline=False)
    fun.add_field(name='-Usage', value='```.luck <message>\n.say <message>\n.color <hex>```', inline=False)
    fun.set_footer(text='Page 4/5')
    fun.set_image(url="https://cdn.discordapp.com/attachments/880030618275156001/890812641201774692/funor_extra.png")
    fun.timestamp=datetime.utcnow()

    developer=discord.Embed(title="5# Developer 🧐", description="```Developer commands!```")
    developer.add_field(name='-Commands', value='```Eval: Evaluates code for you!\nJishaku: A Discord library that runs/debugs code for you!```', inline=False)
    developer.add_field(name='-Usage', value='```.eval <code>\n.jsk <code>```', inline=False)
    developer.set_footer(text='Page 5/5')
    developer.set_image(url="https://cdn.discordapp.com/attachments/880030618275156001/890808937425825873/dev.png")
    developer.timestamp=datetime.utcnow()

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = [info, mod, websites, fun, developer]
    await paginator.run(embeds)

def setup(bot):
  bot.add_cog(Help(bot))
