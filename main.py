from utils.bot import Bonbons
import os

bot = Bonbons()

if __name__ == "__main__":
    bot.run(os.environ["token"])
