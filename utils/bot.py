from .help_command import HelpCommand
from .survive import survive
from datetime import datetime
from disnake.ext import commands
import disnake
import aiohttp
import utils
import os


def human_join(seq, delim=', ', final='or'):
    size = len(seq)
    if size == 0:
        return ''

    if size == 1:
        return seq[0]

    if size == 2:
        return f'{seq[0]} {final} {seq[1]}'

    return delim.join(seq[:-1]) + f' {final} {seq[-1]}'


class Bonbons(commands.Bot):
    def __init__(self, **kwargs):

        super().__init__(
            command_prefix=".",
            case_insensitive=True,
            test_guilds=[
                880030618275155998,  # Kayle's hub
                581139467381768192,  # Cosmo's Lounge
            ],
            intents=disnake.Intents.all(),
            allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False),
            help_command=HelpCommand(),
            strip_after_prefix=True,
            **kwargs,
        )
        self.uptime = datetime.utcnow().timestamp()
        self.used_commands = 0
        self.client = utils.Together(self)

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

        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

        for filename in os.listdir("cogs/groups"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.groups.{filename[:-3]}")

    async def find(self, db, key, value):
        data = await db.find_one({key: value})

        if not data:
            return None

        return data

    async def on_command_error(self, ctx: commands.Context, error: str):

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            _missing_args = list(ctx.command.clean_params)
            missing_args = [f'`{arg}`' for arg in _missing_args[_missing_args.index(error.param.name):]]
            return await ctx.send(f'You are missing the following required arguments: {human_join(missing_args)}')

        elif isinstance(error, disnake.Forbidden):
            await ctx.send(error)

        else:
            await ctx.reply(error)
            raise error
