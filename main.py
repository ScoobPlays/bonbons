import os
from utils.bonbons import Bonbons

bot = Bonbons()

if __name__ == "__main__":
    bot.run(os.environ["token"])
