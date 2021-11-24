import os
from utils.bonbons import Bonbons
from together import Together
from utils.secrets import afk as afk_db
from datetime import datetime

bot = Bonbons()
client = Together(bot)

if __name__ == "__main__":
    bot.run(os.environ["token"])
