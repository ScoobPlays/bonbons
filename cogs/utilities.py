import disnake
from disnake.ext import commands
from pyston import PystonClient, File
from utils.utils import created_at
import re
import asyncio
from typing import Union, Optional


class Utilities(commands.Cog, description="Utilities for the bot."):
    def __init__(self, bot):
        self.pysclient = PystonClient()
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")
        self.bot = bot
        self.last = None

    async def find_thread(ctx: commands.Context, name: str):
        try:
            threads = []
            for channel in ctx.guild.text_channels:
                for thread in channel.threads:
                    if thread.name.startswith(name) or thread.name == name:
                        threads.append(thread.mention)
            await ctx.send(", ".join(threads))
        except Exception:
            await ctx.send(
                embed=disnake.Embed(
                    description=f"No threads were found.",
                    color=disnake.Color.red(),
                )
            )

    @commands.group()
    async def thread(self, ctx: commands.Context):
        """Base command for thread."""
        pass

    @thread.command()
    async def find(self, ctx: commands.Context, *, name: str):

        """Searches the guild for a thread."""

        await self.find_thread(ctx, name)

    @thread.command()
    @commands.has_permissions(manage_channels=True)
    async def massdelete(self, ctx: commands.Context):
        """Deletes every thread in the guild."""
        for channel in ctx.guild.text_channels:
            for thread in channel.threads:
                await thread.delete()
                await ctx.message.add_reaction("✅")

    async def run_code(self, ctx: commands.Context, code: Optional[str]):
        matches = self.regex.findall(code)
        code = matches[0][2]
        lang = matches[0][0] or matches[0][1]

        if not lang:
            return await ctx.reply(
                embed=disnake.Embed(
                    description="No language was hinted.", color=disnake.Color.red()
                )
            )
        output = await self.pysclient.execute(str(lang), [File(code)])

        msg = await ctx.reply(
            embed=disnake.Embed(description=output, color=disnake.Color.greyple())
        )
        self.last = msg

    async def on_run_code(self, before: Optional[str], after: Optional[str]):
        await after.clear_reactions()
        await self.last.delete()

        if after.content.startswith(".run"):
            after = after.content.split(".run")

        matches = self.regex.findall("".join(after[1]))
        code = matches[0][2]
        lang = matches[0][0] or matches[0][1]

        if not lang:
            return await before.reply(
                embed=disnake.Embed(
                    description="No language was hinted.", color=disnake.Color.red()
                )
            )
        output = await self.pysclient.execute(str(lang), [File(code)])

        await before.reply(
            embed=disnake.Embed(description=output, color=disnake.Color.greyple())
        )

    @commands.command()
    async def run(self, ctx: commands.Context, *, code: str):
        """Runs code, must be typehinted with a language and in a codeblock."""
        await self.run_code(ctx, code)

    @commands.Cog.listener()
    async def on_message_edit(self, before: str, after: str):
        if before.content.startswith(".run") and after.content.startswith(".run"):
            await after.add_reaction("🔁")

        def check(reaction, user):
            return user == after.author and str(reaction.emoji) == "🔁"

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=30, check=check
            )
        except asyncio.TimeoutError:
            try:
                await after.clear_reactions()
            except:
                await before.clear_reactions()
        else:
            await self.on_run_code(before, after)

    @commands.command()
    async def echo(
        self,
        ctx,
        channel: Optional[disnake.abc.GuildChannel],
        member: disnake.User,
        *,
        message: Union[str, int],
    ):
        """
        Echo's a message.

        .echo <channel> <user> <message>

        .echo <user> <message>

        """

        channel = channel or ctx.channel

        await ctx.message.delete()
        avatar = await member.display_avatar.with_static_format("png").read()
        webhook = await channel.create_webhook(name=member.name, avatar=avatar)
        await webhook.send(message)
        await webhook.delete()

    @commands.command(name="say", help="Says whatever you want for you.")
    async def say(self, ctx: commands.Context, *, argument: str):
        await ctx.send(argument)

    @commands.command()
    async def snowflake(self, ctx: commands.Context, argument: str) -> None:

        """Displays a snowflake's creation date."""

        embed = disnake.Embed(
            description=f"Snowflake was created at {created_at(argument)}",
            color=disnake.Color.greyple(),
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
