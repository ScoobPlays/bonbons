from .bot import Bonbons

bot = Bonbons()

prefix = bot.mongo["discord"]["prefix"]
messages = bot.mongo["discord"]["messages"]
