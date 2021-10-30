import disnake
from disnake.ext import commands
import aiohttp
from .help_command import MyHelp

class Bonbons(commands.Bot):
    def __init__(self):

        super().__init__(
            command_prefix=".",
            test_guilds=[880030618275155998],
            case_insensitive=True,
            intents=disnake.Intents.all(),
            allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False),
            help_command=MyHelp(),
            strip_after_prefix=True,
            status=disnake.Status.dnd,
            activity=disnake.Game(name="/ commands (soon)"),
            )

    async def on_ready(self):
        print(f"Logged in as {self.user} Ping: {round(self.latency * 1000)}")

        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession(loop=self.loop)
