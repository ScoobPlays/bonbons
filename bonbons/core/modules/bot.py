from disnake import (ApplicationCommandInteraction, ChannelType, Color, Embed,
                     Guild, Message, PartialEmoji)
from disnake.ext.commands import (Bot, Cog, Context, check, command,
                                  slash_command)

class Bot(Cog, description="Commands related to me."):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = self.bot.mongo["discord"]["bot"]
        self.prefix = self.bot.mongo["discord"]["prefixes"]

    @property
    def emoji(self) -> str:
        return PartialEmoji(name='pfp', id=942408031071793203)

    @Cog.listener("on_message")
    async def prefix_ping(self, message: Message):

        if message.channel.type == ChannelType.private:
            return

        prefix = await self.prefix.find_one({"_id": message.guild.id})

        if message.content in [f"<@!{self.bot.user.id}>", f"<@{self.bot.user.id}>"]:
            await message.reply(
                f'Boop! My prefix for this server is `{prefix["prefix"]}`',
                mention_author=False,
            )

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        data = await self.prefix.find_one({"_id": guild.id})

        if data is None:
            await self.prefix.insert_one({"_id": guild.id, "prefix": "."})

        if data is not None:
            pass

    @command()
    @check(
        lambda ctx: ctx.author.id == 534738044004335626
        or ctx.author.id == 656073353215344650
    )
    async def prefix(self, ctx: Context, *, prefix: str):

        """Sets a prefix for the server."""

        try:
            await self.prefix.update_one(
                {"_id": ctx.guild.id}, {"$set": {"prefix": prefix}}
            )

            await ctx.send(
                f'I have changed the current server\'s prefix to "{prefix}".'
            )
        except Exception:
            msg = await ctx.send(f"Prefix was too long, but I changed it.")

    @command(
        aliases=[
            "uptime",
        ]
    )
    async def info(self, ctx: Context):

        """Tells you my information."""

        users = len(self.bot.users)
        guilds = len(self.bot.guilds)

        embed = Embed(
            title="Info",
            color=Color.blurple(),
            description=f"{guilds:,} guilds, {users:,} users.",
        )

        embed.add_field(
            name="Commands",
            value=f"**{self.bot.invoked_commands}** commands have been invoked.",
        )
        embed.add_field(
            name="Uptime",
            value=f"<t:{int(self.bot.uptime)}:F> (<t:{int(self.bot.uptime)}:R>)",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command()
    async def cleanup(self, ctx: Context, limit: int = 5):

        """Cleanup my messages."""

        messages = await ctx.channel.purge(
            limit=limit, check=lambda m: m.author.id == self.bot.user.id
        )

        msg = (
            f'Deleted {len(messages)} {"messages." if len(messages)>1 else "message."}'
        )

        await ctx.send(msg, delete_after=6)
        await ctx.message.add_reaction("✅")

    @command(name="ping")
    async def ping(self, ctx: Context) -> None:

        """Tells you my latency."""

        latency = f"`{self.bot.latency * 1000:.2f}`ms"

        await ctx.reply(latency, mention_author=False)

    @slash_command(name="ping")
    async def ping_slash(self, interaction: ApplicationCommandInteraction) -> None:

        """Tells you my latency"""

        latency = f"`{self.bot.latency * 1000:.2f}`ms"

        await interaction.response.send_message(latency, ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(Bot(bot))
