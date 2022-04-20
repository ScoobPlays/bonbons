import discord
from discord.ext.commands import Cog, Context, command
from utils.bot import Bonbons


class Bot(Cog):

    """
    A cog for commands related to me.
    """

    def __init__(self, bot: Bonbons) -> None:
        self.bot = bot

    @property
    def emoji(self) -> str:
        return "🤖"

    @Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        self.bot.generator.train(message.content)
        self.bot.messages[message.id] = message

    @command(name="log")
    async def log(self, ctx: Context, start: str = None):
        """
        Generates text.
        """

        result = self.bot.generator.generate_text(start)
        await ctx.send(result)

    @command(name="information", aliases=("uptime", "info"))
    async def info(self, ctx: Context) -> None:

        """Tells you my information."""

        users = len(self.bot.users)
        guilds = len(self.bot.guilds)

        embed = discord.Embed(title="Info", color=discord.Color.blurple())

        embed.description = f"• Guilds: {guilds:,}\n• Users: {users:,}\n• Uptime: <t:{int(self.bot.uptime)}:F> (<t:{int(self.bot.uptime)}:R>)\n• Latency: {int(self.bot.latency * 1000):.2f}ms"
        await ctx.send(embed=embed)

    @command(name="ping")
    async def ping(self, ctx: Context) -> None:

        """Tells you my latency."""

        latency = f"{self.bot.latency * 1000:.2f}ms"

        await ctx.send(latency)


async def setup(bot: Bot):
    print("Loaded: Bot")
    await bot.add_cog(Bot(bot))
