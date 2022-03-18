import os

import discord
from aiohttp import ClientSession
from discord.ext import commands

from .help.help_command import CustomHelpCommand

EXTENSIONS = (
    f'cogs.{ext[:-3]}'
    for ext in 
    os.listdir('./cogs')
    if ext.endswith('.py')
)

class Bonbons(commands.Bot):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            command_prefix="b!",
            case_insensitive=True,
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
            help_command=CustomHelpCommand(),
            strip_after_prefix=True,
            **kwargs,
        )
        self._uptime = discord.utils.utcnow().timestamp()

    @property
    def uptime(self) -> int:
        return int(self._uptime) or discord.utils.utcnow()

    async def start(self) -> None:
        await super().start(os.environ["token"])

    async def setup_hook(self) -> None:

        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
        os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
        os.environ["JISHAKU_HIDE"] = "True"

        await self.load_extension("jishaku")

        for extension in EXTENSIONS:
            try:
                await self.load_extension(extension)
            except Exception as err:
                print(f"Failed to load extension {extension}: {err}")

    async def on_ready(self) -> None:

        if not hasattr(self, "session"):
            self.session = ClientSession(loop=self.loop)

        print("Logged in.")
