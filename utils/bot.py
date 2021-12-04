from .help_command import HelpCommand
from .survive import survive
from datetime import datetime
from disnake.ext import commands
import disnake
import aiohttp
import os


class Bonbons(commands.Bot):
    def __init__(self, **kwargs):

        super().__init__(
            command_prefix=".",
            case_insensitive=True,
            test_guilds=[880030618275155998],  # Kayle's hub
            intents=disnake.Intents.all(),
            allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False),
            help_command=HelpCommand(),
            strip_after_prefix=True,
            **kwargs,
        )
        self.uptime = datetime.utcnow().timestamp()
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        self.used_commands = 0

    async def on_ready(self):
        print(f"Logged in as {self.user} Ping: {round(self.latency * 1000)}")

        survive()
        os.environ["JISHAKU_FORCE_PAGINATOR"] = "1"
        os.environ["JISHAKU_PY_RES"] = "false"
        os.environ["JISHAKU_EMBEDDED_JSK"] = "1"
        os.environ["JISHAKU_EMBEDDED_JSK_COLOUR"] = "0x99aab5"
        os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
        os.environ.setdefault("JISHAKU_HIDE", "1")
        self.load_extension("jishaku")

        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession(loop=self.loop)

    def load(self):
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

        for filename in os.listdir("cogs/groups"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.groups.{filename[:-3]}")

    async def on_command_error(self, ctx: commands.Context, error: str):

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)

        elif isinstance(error, disnake.Forbidden):
            await ctx.send(error)

        else:
            await ctx.reply(error)
            raise error


bot = Bonbons()
