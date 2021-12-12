from utils.bot import Bonbons
from utils.together import Together
import os

bot = Bonbons()
bot.client = Together(bot)

if __name__ == "__main__":
    bot.run(os.environ["token"])
