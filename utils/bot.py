import os
from datetime import datetime

import discord
from aiohttp import ClientSession
from discord.ext import commands
from motor import motor_asyncio
from tortoise import Tortoise

from .help.help_command import CustomHelpCommand


class Bonbons(commands, Bot):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            command_prefix=self._get_prefix,
            case_insensitive=True,
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
            help_command=CustomHelpCommand(),
            strip_after_prefix=True,
            **kwargs,
        )
        self.uptime = datetime.now().timestamp()
        self.invoked_commands = 0
        self.mongo = motor_asyncio.AsyncIOMotorClient(os.environ.get("mongo_token"))

    async def start(self) -> None:
        self.setup()
        await super().start(os.environ["token"])

    def setup(self) -> None:

        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
        os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
        os.environ["JISHAKU_HIDE"] = "True"

        self.load_extension("jishaku")

        for ext in os.listdir("./cogs"):
            if ext.endswith(".py"):
                self.load_extension(f"cogs.{ext[:-3]}")

    async def on_ready(self) -> None:

        if not hasattr(self, "session"):
            self.session = ClientSession(loop=self.loop)

        await Tortoise.init(
            db_url="sqlite://db.sqlite3", modules={"models": ["utils.models"]}
        )
        await Tortoise.generate_schemas()

        print("Logged in.")

    async def _get_prefix(
        self, bot: commands.Bot, message: discord.Message
    ) -> commands.when_mentioned_or:

        if isinstance(message.channel, discord.DMChannel):
            return commands.when_mentioned_or(".")(bot, message)

        db = self.mongo["discord"]["prefixes"]
        prefix = await db.find_one({"_id": message.guild.id})

        return commands.when_mentioned_or(prefix["prefix"])(bot, message)
