import os
from utils.bonbons import Bonbons
from together import Together

bot = Bonbons()
client = Together(bot)

@bot.command()
async def calc(ctx, arg):
    await ctx.reply(eval(arg.strip().replace("x", "*")))


if __name__ == "__main__":
    bot.run(os.environ["token"])