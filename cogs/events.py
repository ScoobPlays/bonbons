import disnake
from disnake.ext import commands
import contextlib


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        guild = self.bot.get_guild(880030618275155998)
        general = guild.get_channel(880387280576061450)
        member_role = guild.get_role(880030723908722729)

        await self.bot.wait_until_ready()

        await member.add_roles(member_role)
        await general.send(
            embed=disnake.Embed(
                title="Welcome!",
                description=f"{member.mention} joined! Hope you stay!!",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        guild = self.bot.get_guild(880030618275155998)
        general = guild.get_channel(880387280576061450)

        await self.bot.wait_until_ready()

        await general.send(
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
            self.bot.get_channel(907474389195456622).send(error)
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
                delete_after=4.0,
            )
            with contextlib.suppress(disnake.Forbidden):
                await message.author.edit(nick=message.author.display_name[6:])

        for mention in message.mentions:
            if msg := self.bot.cache["afk"].get(mention.id):
                await message.channel.send(f"{mention.display_name} is AFK: {msg}")


def setup(bot):
    bot.add_cog(Events(bot))
