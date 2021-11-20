from disnake import (
    Embed,
    Color
)
from disnake.ext import commands
from pyston import PystonClient, File
import re


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.pysclient = PystonClient()
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")

    async def run_code(self, ctx: commands.Context, code: str):
        matches = self.regex.findall(code)
        code = matches[0][2]
        lang = matches[0][0] or matches[0][1]

        if not code:
            return await ctx.send(
                embed=Embed(
                    description="The code was nonexistent.", color=Color.red()
                )
            )

        if not lang:
            return await ctx.send(
                embed=Embed(
                    description="No language was hinted.", color=Color.red()
                )
            )
        output = await self.pysclient.execute(str(lang), [File(code)])

        await ctx.send(
            embed=Embed(description=output, color=Color.greyple())
        )

    @commands.command()
    async def run(self, ctx: commands.Context, *, code: str):
        """Runs code, must be typehinted with a language and in a codeblock."""
        await self.run_code(ctx, code)


def setup(bot):
    bot.add_cog(Utilities(bot))
