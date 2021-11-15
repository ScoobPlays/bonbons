import os
from utils import Bonbons
from together import Together

bot = Bonbons()
client = Together(bot)

if __name__ == "__main__":
    bot.run(os.environ["token"])