from keep_alive import keep_alive
from .help_command import HelpCommand
from cogs.dev import Calculator
from datetime import datetime
from disnake.ext import commands
import disnake
import aiohttp
import os

class Bonbons(commands.Bot):
    def __init__(self, **kwargs):

        super().__init__(
            command_prefix=".",
            test_guilds=[
                880030618275155998, #Kayle's Hub
                912724631616651294, #Feou's Server
                ],
            case_insensitive=True,
            intents=disnake.Intents.all(),
            allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False),
            help_command=HelpCommand(),
            strip_after_prefix=True,
            **kwargs
            )
        self.persistent_views_added = False

    async def on_ready(self):
        print(f"Logged in as {self.user} Ping: {round(self.latency * 1000)}")

        if not self.persistent_views_added:
            self.add_view(Calculator())
            self.persistent_views_added = True

        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

        keep_alive()
        os.environ["JISHAKU_FORCE_PAGINATOR"] = "1"
        os.environ['JISHAKU_PY_RES'] = 'false'
        os.environ["JISHAKU_EMBEDDED_JSK"] = "1"
        os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
        os.environ.setdefault("JISHAKU_HIDE", "1")
        self.load_extension("jishaku")

        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession(loop=self.loop)

bot = Bonbons()
bot.uptime = datetime.utcnow().timestamp()