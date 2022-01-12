from .help_command import HelpCommand
from .survive import survive
from datetime import datetime
from disnake.ext.commands import (
    Bot,
    Context,
    CommandNotFound,
    MissingRequiredArgument,
    DisabledCommand,
    CheckFailure,
    CommandOnCooldown,
    when_mentioned_or,
)
from disnake import Intents, AllowedMentions, Forbidden, Message, Activity, ActivityType
from motor import motor_asyncio
from aiohttp import ClientSession
import os


class Bonbons(Bot):
    def __init__(self, **kwargs):

        super().__init__(
            command_prefix=self.get_prefix_from_db,
            case_insensitive=True,
            test_guilds=[
                880030618275155998,
                581139467381768192,
                926115595307614249,
            ],
            intents=Intents.all(),
            allowed_mentions=AllowedMentions(everyone=False, roles=False),
            help_command=HelpCommand(),
            strip_after_prefix=True,
            activity=Activity(type=ActivityType.listening, name="you ❤️"),
            **kwargs,
        )
        self.uptime = datetime.now().timestamp()
        self.invoked_commands = 0
        self.mongo = motor_asyncio.AsyncIOMotorClient(os.environ.get("mongo_token"))

    def run(self):
        self.setup()
        super().run(os.environ["token"], reconnect=True)

    def setup(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

        for filename in os.listdir("./cogs/groups"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.groups.{filename[:-3]}")

    async def on_ready(self):

        survive()
        os.environ["JISHAKU_FORCE_PAGINATOR"] = "1"
        os.environ["JISHAKU_PY_RES"] = "false"
        os.environ["JISHAKU_EMBEDDED_JSK"] = "1"
        os.environ["JISHAKU_EMBEDDED_JSK_COLOUR"] = "0x2F3136"
        os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
        os.environ.setdefault("JISHAKU_HIDE", "1")
        self.load_extension("jishaku")

        self.session = ClientSession(loop=self.loop)
        print('Logged in.')

    async def get_prefix_from_db(self, bot: Bot, message: Message):
        db = self.mongo["discord"]["prefix"]

        prefix = await db.find_one({"_id": message.guild.id})
        try:
            return prefix["prefix"]
        except TypeError:
            return "."

    async def on_command_error(self, ctx: Context, error: Exception):

        if isinstance(error, CommandNotFound):
            return

        elif isinstance(error, MissingRequiredArgument):
            return await ctx.reply(
                f"```\n{ctx.command.name} {ctx.command.signature}\n```\nNot enough arguments passed.",
                mention_author=False,
            )

        elif isinstance(error, DisabledCommand):
            return await ctx.reply(
                "This command has been disabled.", mention_author=False
            )

        elif isinstance(error, CommandOnCooldown):
            return await ctx.reply(
                "You have already used this command earlier. Try again later.",
                mention_author=False,
            )

        elif isinstance(error, CheckFailure):
            return await ctx.reply("You cannot use this command.", mention_author=False)

        elif isinstance(error, Forbidden):
            return await ctx.reply("I cannot run this command.", mention_author=False)

        else:
            await ctx.reply(error)
            raise error
