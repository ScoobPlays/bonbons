import os
from datetime import datetime

from aiohttp import ClientSession
from disnake import (
    Activity,
    ActivityType,
    AllowedMentions,
    DMChannel,
    Forbidden,
    Intents,
    Message,
)
from disnake.ext.commands import (
    Bot,
    CheckFailure,
    CommandNotFound,
    CommandOnCooldown,
    Context,
    DisabledCommand,
    MissingRequiredArgument,
    when_mentioned_or,
)
from motor import motor_asyncio

from .help.help_command import CustomHelpCommand

# TODO: Implement caching in `get_prefix_from_database`


class Bonbons(Bot):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            command_prefix=self.get_prefix_from_db,
            case_insensitive=True,
            intents=Intents.all(),
            allowed_mentions=AllowedMentions(everyone=False, roles=False),
            help_command=CustomHelpCommand(),
            strip_after_prefix=True,
            **kwargs,
        )
        self.uptime = datetime.now().timestamp()
        self.invoked_commands = 0
        self.mongo = motor_asyncio.AsyncIOMotorClient(os.environ.get("mongo_token"))
        self._prefix_cache = {}

    def run(self) -> None:
        self.setup()
        super().run(os.environ["token"], reconnect=True)

    def setup(self) -> None:

        os.environ["JISHAKU_FORCE_PAGINATOR"] = "1"
        os.environ["JISHAKU_PY_RES"] = "false"
        os.environ["JISHAKU_EMBEDDED_JSK"] = "1"
        os.environ["JISHAKU_EMBEDDED_JSK_COLOUR"] = "0x2F3136"
        os.environ["JISHAKU_NO_UNDERSCORE"] = "1"
        self.load_extension("jishaku")

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self) -> None:

        if not hasattr(self, "session"):
            self.session = ClientSession(loop=self.loop)

        print("Logged in.")

    async def get_prefix_from_db(self, bot: Bot, message: Message):

        if isinstance(message.channel, DMChannel):
            return when_mentioned_or(".")(bot, message)

        db = self.mongo["discord"]["prefixes"]

        prefix = await db.find_one({"_id": message.guild.id})

        self._prefix_cache = prefix["prefix"]

        return when_mentioned_or(prefix["prefix"])(bot, message)

    @staticmethod
    async def on_command_error(self, ctx: Context, error: Exception) -> None:

        if isinstance(error, CommandNotFound):
            return

        if isinstance(error, MissingRequiredArgument):
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
