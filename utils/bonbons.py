import os
from disnake.ext import commands
import disnake
import aiohttp
from keep_alive import keep_alive
from .help_command import MyHelp

class Bonbons(commands.Bot):
    def __init__(self, **kwargs):

        super().__init__(
            command_prefix=".",
            test_guilds=[880030618275155998, 581139467381768192],
            case_insensitive=True,
            intents=disnake.Intents.all(),
            allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False),
            help_command=MyHelp(),
            strip_after_prefix=True,
            status=disnake.Status.dnd,
            **kwargs
            )

    async def on_ready(self):
        print(f"Logged in as {self.user} Ping: {round(self.latency * 1000)}")

        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")
       
        self.cache = {"afk":{}}

        keep_alive()
        os.environ["JISHAKU_FORCE_PAGINATOR"] = "1"
        os.environ["JISHAKU_EMBEDDED_JSK"] = "1"
        os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
        os.environ.setdefault("JISHAKU_HIDE", "1")
        self.load_extension("jishaku")

        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession(loop=self.loop)
