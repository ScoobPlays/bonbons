from disnake import Color, Embed
from disnake.ext import commands
import re


class Evaluation(commands.Cog, description="Commands that evaluate code."):
    def __init__(self, bot):
        self.bot = bot
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")

    @property
    def session(self):
        return self.bot.http._HTTPClient__session

    async def _run_code(self, *, lang: str, code: str):
        res = await self.session.post(
            "https://emkc.org/api/v1/piston/execute",
            json={"language": lang, "source": code},
        )
        return await res.json()

    @commands.command()
    async def run(self, ctx: commands.Context, *, codeblock: str):
        """
        Runs code.
        """
        matches = self.regex.findall(codeblock)
        if not matches:
            return await ctx.reply(
                embed=Embed(
                    description="Couldn't quite see your codeblock.", color=Color.red()
                )
            )
        lang = matches[0][0] or matches[0][1]
        if not lang:
            return await ctx.reply(
                embed=Embed(
                    description="Couldn't find the language hinted in the codeblock or before it.",
                    color=Color.red(),
                )
            )
        code = matches[0][2]
        result = await self._run_code(lang=lang, code=code)

        await self._send_result(ctx, result)

    @commands.command()
    async def runl(self, ctx: commands.Context, lang: str, *, code: str):
        """
        Run a single line of code.
        """
        result = await self._run_code(lang=lang, code=code)
        await self._send_result(ctx, result)

    async def _send_result(self, ctx: commands.Context, result: dict):
        if "message" in result:
            return await ctx.reply(
                embed=Embed(description=result["message"], color=Color.red())
            )

        output = result["output"]
        language = result["language"]

        embed = Embed(color=Color.green())
        output = output[:500].strip()
        shortened = len(output) > 500
        lines = output.splitlines()
        shortened = shortened or (len(lines) > 15)
        output = "\n".join(lines[:15])
        output += shortened * ""
        if not output:
            embed.add_field(name="Output", value=f"```[No output]```")

        if output:
            embed.add_field(
                name="Output",
                value=f"```{language}\n{output}\n```" or "**[No output]**",
            )

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Evaluation(bot))
