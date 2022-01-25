import disnake
from disnake.ext import commands


class Advertising(disnake.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Invite Me",
                url="https://discordapp.com/oauth2/authorize?client_id=888309915620372491&scope=bot+applications.commands&permissions=0",
            )
        )
        self.bot = bot

    @disnake.ui.button(label="Recent Commands")
    async def rc(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.defer()

        commands_usage = []
        DELIMITER = "\n"

        for result in self.bot.LAST_COMMANDS_USAGE[-5:]:
            commands_usage.append(
                f"<t:{result['timestamp']}:R>: {result['mention'].mention}"
            )

        embede = disnake.Embed(
            title="Recent Command Usages",
            description=DELIMITER.join(commands_usage) or "No commands have been used.",
            color=disnake.Color.blurple(),
        )

        await interaction.edit_original_message(embed=embede)


class Bot(commands.Cog):
    """Bot-related commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = self.bot.mongo["discord"]["bot"]
        self.prefix = self.bot.mongo["discord"]["prefixes"]
        self.emoji = "🤖"

    @commands.Cog.listener("on_message")
    async def prefix_ping(self, message: disnake.Message):

        if message.channel.type == disnake.ChannelType.private:
            return

        prefix = await self.prefix.find_one({"_id": message.guild.id})

        if message.content in [f"<@!{self.bot.user.id}>", f"<@{self.bot.user.id}>"]:
            await message.reply(
                f'Boop! My prefix for this server is `{prefix["prefix"]}`',
                mention_author=False,
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        data = await self.prefix.find_one({"_id": guild.id})

        if data is None:
            await self.prefix.insert_one({"_id": guild.id, "prefix": "."})

        if data is not None:
            pass

    @commands.command()
    @commands.check(
        lambda ctx: ctx.author.id == 534738044004335626
        or ctx.author.id == 656073353215344650
    )
    async def prefix(self, ctx: commands.Context, *, prefix: str):

        """Sets a prefix for the current server."""

        try:
            await self.prefix.update_one(
                {"_id": ctx.guild.id}, {"$set": {"prefix": prefix}}
            )

            await ctx.send(
                f'I have changed the current server\'s prefix to "{prefix}".'
            )
        except Exception:
            msg = await ctx.send(f"Prefix was too long, but I changed it.")

    @commands.command(
        aliases=[
            "uptime",
        ]
    )
    async def info(self, ctx: commands.Context):

        """Returns the bots information."""

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
        await ctx.send(embed=embed, view=Advertising(self.bot))

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
