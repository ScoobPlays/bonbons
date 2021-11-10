import disnake
from disnake.ext import commands
import contextlib


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.general = self.bot.get_guild(880030618275155998).get_channel(880387280576061450)
        self.member = self.bot.get_guild(880030618275155998).get_role(880030723908722729)

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):

        await self.bot.wait_until_ready()

        if member.guild.id != 880030618275155998:
            pass

        await member.add_roles(self.member)
        await self.general.send(
            embed=disnake.Embed(
                title="Welcome!",
                description=f"{member.mention} joined! Hope you stay!!",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):

        await self.bot.wait_until_ready()

        await self.general.send(
            embed=disnake.Embed(
                title="Goodbye!",
                description=f"{member.mention} left.. :cry:",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: str):

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(error, mention_author=False)

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=disnake.Embed(
                    title="Missing Required Argument",
                    description=error,
                    color=disnake.Color.red(),
                ),
                mention_author=False,
            )

        else:
            a = self.bot.get_channel(
                907474389195456622
            ) or await self.bot.fetch_channel(907474389195456622)
            await a.send(error)
            await ctx.reply("An error has occured.")
            raise error

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):

        if message.author.bot:
            return

        if message.author.id in self.bot.cache["afk"].keys():
            del self.bot.cache["afk"][message.author.id]
            await message.channel.send(
                f"Welcome back {message.author.display_name}!",
                delete_after=5.0,
            )
            with contextlib.suppress(disnake.Forbidden):
                await message.author.edit(nick=message.author.display_name[6:])

        for mention in message.mentions:
            if msg := self.bot.cache["afk"].get(mention.id):
                await message.channel.send(f"{mention.display_name} is AFK: {msg}")


def setup(bot):
    bot.add_cog(Events(bot))
