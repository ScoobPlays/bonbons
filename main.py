import os
from utils.bonbons import Bonbons
from utils.together import Together

bot = Bonbons()
client = Together(bot)

if __name__ == "__main__":
    bot.run(os.environ["token"])