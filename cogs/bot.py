import traceback

import discord
from discord.ext import commands


class Bot(commands.Cog):

    """
    Commands related to me.
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
    @commands.command(name="invite")
    async def invite(self, ctx: commands.Context) -> None:

        """Sends you my invite link!"""

        invite = discord.ui.View()
        invite.add_item(
            discord.ui.Button(
                label="Invite Me!",
                style=discord.ButtonStyle.url,
                url="https://discord.com/api/oauth2/authorize?client_id=888309915620372491&permissions=412387494464&scope=bot",
            )
        )

        try:
            await ctx.author.send(
                "Click the button below to invite me to your discord server!"
            )
            await ctx.message.add_reaction("✅")
        except discord.Forbidden:
            await ctx.message.add_reaction("❌")
            return await ctx.send("Message failed to send. Are your DMs open?")

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
        )
        embed.add_field(name="Guilds", value=f"{guilds:,}")
        embed.add_field(name="Users", value=f"{users:,}")
        embed.add_field(
            name="Uptime",
            value=f"<t:{int(self.bot.uptime)}:F> (<t:{int(self.bot.uptime)}:R>)",
        )
        embed.add_field(
            name="Ping",
            value=f"{int(self.bot.latency * 1000):.2f}ms",
        )
        await ctx.send(embed=embed)


    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:

        """Tells you my latency."""

        latency = f"{self.bot.latency * 1000:.2f}ms"

        await ctx.send(latency)


async def setup(bot: Bot):
    await bot.add_cog(Bot(bot))
