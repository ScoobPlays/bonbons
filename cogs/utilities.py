import disnake
from disnake.ext import commands
from pyston import PystonClient, File
from utils.utils import created_at
import re


class Utilities(commands.Cog, description="Utilities for the bot."):
    def __init__(self, bot):
        self.pysclient = PystonClient()
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")

    async def run_code(self, ctx: commands.Context, code: str):
        matches = self.regex.findall(code)
        code = matches[0][2]
        lang = matches[0][0] or matches[0][1]

        if not code:
            return await ctx.send(
                embed=disnake.Embed(
                    description="The code was nonexistent.", color=disnake.Color.red()
                )
            )

        if not lang:
            return await ctx.send(
                embed=disnake.Embed(
                    description="No language was hinted.", color=disnake.Color.red()
                )
            )
        output = await self.pysclient.execute(str(lang), [File(code)])

        await ctx.send(
            embed=disnake.Embed(description=output, color=disnake.Color.greyple())
        )

    @commands.command()
    async def run(self, ctx: commands.Context, *, code: str):
        """Runs code, must be typehinted with a language and in a codeblock."""
        await self.run_code(ctx, code)

    @commands.command()
    async def echo(self, ctx, member: disnake.Member, *, message):
        """Echo's a message. Member is a required argument. (pass in a mention/id)"""
        await ctx.message.delete()
        avatar = await member.display_avatar.with_static_format('png').read()
        webhook = await ctx.channel.create_webhook(name=member.name, avatar=avatar)
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