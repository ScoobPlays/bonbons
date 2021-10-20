import disnake
from disnake.ext import commands
import os
from aiohttp import ClientSession

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(">"),
    test_guilds=[880030618275155998],
    case_insensitive=True,
    intents=disnake.Intents.all(),
    allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False),
    strip_after_prefix=True,
)

@bot.event
async def on_ready():
    print(f"Bot is ready to be used! Ping: {round(bot.latency * 1000)}")
    if not hasattr(bot, 'session'):
        bot.session = ClientSession(loop=bot.loop)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

os.environ['JISHAKU_EMBEDDED_JSK'] = '1'
bot.load_extension("jishaku")

if __name__ == "__main__":
  bot.run(os.environ["token"])
