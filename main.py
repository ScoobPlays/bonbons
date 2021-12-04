from utils.bot import Bonbons
from together import Together
import os

bot = Bonbons()
client = Together(bot)
bot.load()

if __name__ == "__main__":
    bot.run(os.environ["token"])
