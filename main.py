import os
from utils.bonbons import Bonbons
from together import Together
from disnake.ext import commands

bot = Bonbons()
client = Together(bot)

@bot.command()
@commands.is_owner()
async def activity(ctx, activity):
    await ctx.send(await client.create_link(ctx.author.voice.channel.id, activity))

if __name__ == "__main__":
    bot.run(os.environ["token"])
