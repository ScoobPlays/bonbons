import os
from utils.bonbons import Bonbons

bot = Bonbons()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

##jishaku/https://github.com/Kraots/jishaku <3
os.environ["JISHAKU_FORCE_PAGINATOR"] = "1"
os.environ["JISHAKU_EMBEDDED_JSK"] = "1"
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
os.environ.setdefault("JISHAKU_HIDE", "1")
bot.load_extension("jishaku")

if __name__ == "__main__":
    bot.run(os.environ["token"])
