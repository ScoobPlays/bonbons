import discord
import os
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    case_insensitive=True,
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
    strip_after_prefix=True,
)
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"Bot is ready to be used! Ping: {round(bot.latency * 1000)}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

keep_alive()
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
os.environ.setdefault("JISHAKU_HIDE", "1")
bot.load_extension("jishaku")

if __name__ == "__main__":
    bot.run(os.environ["token"])
