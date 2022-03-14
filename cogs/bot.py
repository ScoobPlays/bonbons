import discord
from discord.ext import commands


class Bot(commands.Cog):

    """
    Commands related to me.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = self.bot.mongo["discord"]["bot"]
        self.prefixes = self.bot.mongo["discord"]["prefixes"]

    @property
    def emoji(self) -> str:
        return "🤖"

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:

        if message.channel.type == discord.ChannelType.private:
            return

        prefix = await self.prefixes.find_one({"_id": message.guild.id})

        if message.content in [f"<@!{self.bot.user.id}>", f"<@{self.bot.user.id}>"]:
            await message.reply(
                f'Boop! My prefix for this server is `{prefix["prefix"]}`',
            )

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
            print(error)
            await ctx.reply(error)

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: discord.Guild):
        data = await self.prefixes.find_one({"_id": guild.id})

        if data is None:
            await self.prefixes.insert_one(
                {"_id": guild.id, "prefix": self.bot.default_prefix}
            )

        if data is not None:
            pass

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

    @commands.command(name="prefix")
    @commands.check(
        lambda ctx: ctx.author.id == 534738044004335626
        or ctx.author.id == 656073353215344650
    )
    async def prefix(self, ctx: commands.Context, *, prefix: str) -> None:

        """Sets a prefix for the server."""

        try:
            await self.prefixes.update_one(
                {"_id": ctx.guild.id}, {"$set": {"prefix": prefix}}
            )

            await ctx.send(
                f'New prefix set to: "{prefix}".'
            )
        except discord.Forbidden:
            await ctx.message.add_reaction("\U00002705")

    @commands.command(
        aliases=[
            "uptime",
        ]
    )
    async def info(self, ctx: commands.Context) -> None:

        """Tells you my information."""

        users = len(self.bot.users)
        guilds = len(self.bot.guilds)
        commands = f"**{self.bot.invoked_commands}** commands have been invoked." if self.bot.invoked_commands is not None else "N/A"

        embed = discord.Embed(
            title="Info",
            color=discord.Color.blurple(),
            description=f"I can see {guilds:,} guilds, {users:,} users.",
        )

        embed.add_field(
            name="Commands",
            value=commands,
        )
        embed.add_field(
            name="Uptime",
            value=f"<t:{int(self.bot.uptime)}:F> (<t:{int(self.bot.uptime)}:R>)",
            inline=False,
        )
        await ctx.send(embed=embed)


    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:

        """Tells you my latency."""

        latency = f"`{self.bot.latency * 1000:.2f}`ms"

        await ctx.reply(latency, mention_author=False)


async def setup(bot: Bot):
    await bot.add_cog(Bot(bot))