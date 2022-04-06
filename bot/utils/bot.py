import os
from traceback import print_exc

import discord
from aiohttp import ClientSession
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from utils.utils import Generator

EXTENSIONS = (f"cogs.{ext[:-3]}" for ext in os.listdir("./cogs") if ext.endswith(".py"))


class Bonbons(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="b!",
            case_insensitive=True,
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
            strip_after_prefix=True,
        )
        self.uptime: int = int(discord.utils.utcnow().timestamp())
        self.messages: dict[int, discord.Message] = {}
        self.ignored_cogs: list[str] = ["Jishaku", "Owner", "Help"]
        self.generator: Generator = Generator(depth=3)

    async def start(self) -> None:
        await super().start(os.environ["token"])

    async def setup_hook(self) -> None:

        self.mongo = AsyncIOMotorClient(os.environ["mongo_token"])

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

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply(
                f"```\n{ctx.command.name} {ctx.command.signature}\n```\nNot enough arguments passed.",
            )

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.reply("This command has been disabled!")

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.reply(
                "You have already used this command earlier. Try again later.",
                mention_author=False,
            )

        elif isinstance(error, commands.CheckFailure):
            return await ctx.reply("You cannot use this command!")

        elif isinstance(error, discord.Forbidden):
            return await ctx.reply("I cannot run this command.")

        else:
            await ctx.reply("An error has occured. Sorry.")

            print_exc(type(error), error, error.__traceback__)

    def get_message(self, message_id: int) -> discord.Message:
        return self.messages.get(message_id, None)