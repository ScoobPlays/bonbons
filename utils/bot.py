import os
from datetime import datetime

import discord
from aiohttp import ClientSession
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from asyncpraw import Reddit

from .help.help_command import CustomHelpCommand


class Bonbons(commands.Bot):
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
        self.mongo = AsyncIOMotorClient(os.environ.get("mongo_token"))
        self.economy = self.mongo["discord"]["economy"]
        self.default_prefix = "b"
        self.reddit = Reddit(
            client_id="Afm7Vjl071XabpFmf_zHWQ",
            client_secret="Lwr071ALLSLtZd0wkK4szSsPrd6l5Q",
            user_agent="bonbons"
            )
        self._prefixes = self.mongo["discord"]["prefixes"]
        self.memes = []

    async def start(self) -> None:
        await self.setup()
        await super().start(os.environ["token"])

    async def setup(self) -> None:

        await self._cache_memes()
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

        print("Logged in.")

    async def _get_prefix(
        self, bot: commands.Bot, message: discord.Message
    ) -> commands.when_mentioned_or:

        if isinstance(message.channel, discord.DMChannel):
            return commands.when_mentioned_or(self.default_prefix)(bot, message)

        prefix = await self._prefixes.find_one({"_id": message.guild.id})
        
        setattr(self.help_command.context, "prefix", prefix["prefix"])

        return commands.when_mentioned_or(prefix["prefix"])(bot, message)

    async def _cache_memes(self) -> None:

        subreddit = await self.reddit.subreddit("memes")

        async for submission in subreddit.hot(limit=500):
            if submission.url.startswith('https://i.redd.it/'):
                self.memes.append(submission)

        async for submission in subreddit.top(limit=500):
            if submission.url.startswith('https://i.redd.it/'):
                self.memes.append(submission)