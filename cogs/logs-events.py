import disnake
from disnake.ext import commands
import contextlib
from datetime import datetime


class Events(commands.Cog, description="A cog for events/logs."):
    def __init__(self, bot):
        self.bot = bot
        self.logs = self.bot.get_guild(880030618275155998).get_channel(
            907820956733558784
        )
        self.general = self.bot.get_guild(880030618275155998).get_channel(
            880387280576061450
        )
        self.member = self.bot.get_guild(880030618275155998).get_role(
            880030723908722729
        )
        self.errors = self.bot.get_guild(880030618275155998).get_channel(
            907474389195456622
        )

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

        embed = disnake.Embed(
            title="Member Joined",
            description=f"""
            **Member:** {member} ({member.id})
            **Guild:** {member.guild.name} ({member.guild.id})
            **Joined At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
        )
        await self.logs.send(embed=embed)

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

        embed = disnake.Embed(
            title="Member Removed",
            description=f"""
            **Member:** {member} ({member.id})
            **Guild:** {member.guild.name} ({member.guild.id})
            **Left At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
        )
        await self.logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        embed = disnake.Embed(
            title="Message Deleted",
            description=f"""
            **Author:** {message.author.mention} ({message.author.id})
            **Guild:** {message.guild.name} ({message.guild.id})
            **Channel:** {message.channel.mention} ({message.channel.id})
            **Deleted At:** <t:{int(message.created_at.timestamp())}:F> (<t:{int(message.created_at.timestamp())}:R>)
            """,
        ).add_field(name="Message Content", value=message.content)
        await self.logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot and after.author.bot:
            return

        embed = (
            disnake.Embed(
                title="Message Edited",
                description=f"""
            **Author:** {before.author.mention} ({before.author.id})
            **Guild:** {before.guild.name} ({before.guild.id})
            **Channel:** {before.channel.mention} ({before.channel.id})
            **Deleted At:** <t:{int(before.created_at.timestamp())}:F> (<t:{int(before.created_at.timestamp())}:R>)
            """,
            )
            .add_field(name="Before Content", value=before.content, inline=False)
            .add_field(name="After Content", value=after.content, inline=False)
        )
        await self.logs.send(embed=embed)

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
            await self.errors.send(error)
            await ctx.reply(embed=disnake.Embed(description="An error has occured."))
            raise error


def setup(bot):
    bot.add_cog(Events(bot))
