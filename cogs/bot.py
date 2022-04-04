import traceback

import discord
from discord.ext import commands


class Bot(commands.Cog):

    """
    A cog for commands related to me.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @property
    def emoji(self) -> str:
        return "🤖"

    @commands.Cog.listener("on_command_error")
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

            traceback.print_exc(type(error), error, error.__traceback__)

    @commands.command(
        aliases=(
            "uptime",
        )
    )
    async def info(self, ctx: commands.Context) -> None:

        """Tells you my information."""

        users = len(self.bot.users)
        guilds = len(self.bot.guilds)

        embed = discord.Embed(
            title="Info",
            color=discord.Color.blurple()
        )
        
        embed.description = f"""
        • Guilds: {guilds:,}
        • Users: {users:,}
        • Uptime: <t:{int(self.bot.uptime)}:F> (<t:{int(self.bot.uptime)}:R>)
        • Latency: {int(self.bot.latency * 1000):.2f}ms
        """
        await ctx.send(embed=embed)


    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:

        """Tells you my latency."""

        latency = f"{self.bot.latency * 1000:.2f}ms"

        await ctx.send(latency)


async def setup(bot: Bot):
    await bot.add_cog(Bot(bot))
