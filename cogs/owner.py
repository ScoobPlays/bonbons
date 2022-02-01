from disnake.ext import commands
import io
import os
import sys
import textwrap
import traceback
import contextlib
from utils.objects import cleanup_code
import disnake
from utils.paginators import TextPaginator


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.no = "<:no:914859683842523207>"
        self.yes = "<:yes:932551215764607007>"
        self.library_dict = {
            "pycord": disnake,
            "nextcord": disnake,
            "hikari": disnake,
            "cock": disnake,
            "nestcord": disnake,
            "diskord": disnake,
        }

    async def cog_check(self, ctx: commands.Context) -> int:
        return ctx.author.id == 656073353215344650

    async def restart_bot(self, ctx: commands.Context) -> None:
        try:
            await ctx.message.add_reaction("✅")

            os.execv(sys.executable, ["python"] + sys.argv)
        except Exception:
            pass

    @commands.command(aliases=["rs"])
    async def restart(self, ctx: commands.Context) -> None:
        await self.restart_bot(ctx)

    @commands.command(name="eval", aliases=["e"])
    async def _eval(self, ctx: commands.Context, *, code: str):

        variables: dict = {
            "ctx": ctx,
            "bot": self.bot,
            "disnake": disnake,
            "_channel": ctx.channel,
            "_author": ctx.author,
            "_guild": ctx.guild,
            "_message": ctx.message,
            "nl": "\n",
            **globals(),
            **self.library_dict,
        }

        code = cleanup_code(code)
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):

                exec(
                    f'async def _execute_human():\n{textwrap.indent(code, "  ")}',
                    variables,
                )
                obj = await variables["_execute_human"]()
                result = str(obj)

        except Exception as e:
            result = "".join(traceback.format_exception(e, e, e.__traceback__))

        if len(result) >= 4000:
            paginator = TextPaginator(
                ctx, [result[i : i + 4000] for i in range(0, len(result), 4000)]
            )
            return await paginator.start()

        embed = disnake.Embed(
            description=f"```py\n{result}\n```", color=disnake.Color.blurple()
        )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))
