import disnake
from disnake.ext import commands
import utils


class Bot(commands.Cog, description="Commands for the bot."):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.mongo["discord"]["bot"]
        self.prefix = self.bot.mongo["discord"]["prefix"]

    @property
    def emoji(self):
        return "🤖"

    @commands.Cog.listener("on_message")
    async def prefix_ping(self, message: disnake.Message):

        prefix = await self.prefix.find_one({"_id": message.guild.id})

        if (
            message.content == f"<@{self.bot.user.id}>"
            or message.content == f"<@!{self.bot.user.id}>"
        ):
            await message.reply(
                f'Boop! My prefix for this server is `{prefix["prefix"]}`',
                mention_author=False,
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        data = await self.prefix.find_one({"_id": guild.id})

        if data is None:
            await self.prefix.insert_one({"_id": guild.id, "prefix": "."})

        else:
            pass

    @commands.command(name="prefix")
    @commands.is_owner()
    async def prefix(self, ctx: commands.Context, *, prefix: str):

        """Sets a prefix for the current server."""

        await self.prefix.update_one(
            {"_id": ctx.guild.id}, {"$set": {"prefix": prefix}}
        )

        await ctx.send(f"I have changed the prefix to {prefix}")

    @commands.command(
        aliases=(
            "uptime",
            "botinfo",
        )
    )
    async def info(self, ctx: commands.Context):

        """Returns the bots info."""

        embed = disnake.Embed(
            title="My Information",
            color=disnake.Color.blurple(),
            description=f"I have access to {len(self.bot.guilds)} guilds and can see {len(self.bot.users)} users.",
        )

        data = await self.db.find_one({"_id": self.bot.user.id})
        embed.add_field(
            name="Commands", value=f"**{data['uses']}** commands have been invoked."
        )
        embed.add_field(
            name="Uptime",
            value=f"<t:{int(self.bot.uptime)}:F> (<t:{int(self.bot.uptime)}:R>)",
            inline=False,
        )
        await ctx.send(embed=embed, view=utils.Advertising())

    @commands.command()
    async def cleanup(self, ctx: commands.Context, limit: int = 5):
        """Cleanup the bots messages."""

        messages = await ctx.channel.purge(
            limit=limit, check=lambda m: m.author == self.bot.user
        )

        msg = (
            f'Deleted {len(messages)} {"messages." if len(messages)>1 else "message."}'
        )

        await ctx.send(msg, delete_after=6)
        await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Bot(bot))
