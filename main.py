from utils.bonbons import Bonbons
from together import Together
import os

bot = Bonbons()
client = Together(bot)    

"""beg"""
if __name__ == "__main__":
    bot.run(os.environ["token"])
