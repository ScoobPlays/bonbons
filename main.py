import os
from utils.bonbons import Bonbons
from disnake.ext import commands
from together import Together

bot = Bonbons()
bot._BotBase__cogs  = commands.core._CaseInsensitiveDict()
client = Together(bot)    

if __name__ == "__main__":
    bot.run(os.environ["token"])