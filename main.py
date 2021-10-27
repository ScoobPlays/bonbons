import disnake
from disnake.ext import commands
import os
from aiohttp import ClientSession
from keep_alive import keep_alive
from utils.help_command import MyHelp

bot = commands.Bot(
    command_prefix=".",
    test_guilds=[880030618275155998],
    case_insensitive=True,
    intents=disnake.Intents.all(),
    allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False),
    help_command=None,
    strip_after_prefix=True,
    status=disnake.Status.dnd,
    activity=disnake.Game(name="/ commands (soon)"),
)


@bot.event
async def on_ready():
    print(f"Bot is ready to be used! Ping: {round(bot.latency * 1000)}")
    if not hasattr(bot, "session"):
        bot.session = ClientSession(loop=bot.loop)

bot.help_command = MyHelp()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


keep_alive()
os.environ["JISHAKU_FORCE_PAGINATOR"] = "1"
os.environ["JISHAKU_EMBEDDED_JSK"] = "1"
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
os.environ.setdefault("JISHAKU_HIDE", "1")
bot.load_extension("jishaku")

if __name__ == "__main__":
    bot.run(os.environ["token"])
