from disnake.ext import commands
import disnake
import io
import os
import sys
import textwrap
import traceback
import contextlib
from utils.objects import cleanup_code, paginate


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.no = "<:no:914859683842523207>"
        self.yes = "<:yes:932551215764607007>"

    async def cog_check(self, ctx: commands.Context) -> int:
        return ctx.author.id == 656073353215344650

    async def restart_bot(self, ctx: commands.Context) -> None:
        try:
            await ctx.message.add_reaction("✅")

            os.execv(sys.executable, ["python"] + sys.argv)
        except Exception:
            await ctx.author.send(
                embed=disnake.Embed(
                    description="Bot failed to restart.", color=disnake.Color.red()
                )
            )
            await ctx.message.add_reaction(":x:")

    async def _execute_children(self, ctx: commands.Context, code: str):
        vars: dict = {
            "ctx": ctx,
            "bot": self.bot,
            "_channel": ctx.channel,
            "_author": ctx.author,
            "_guild": ctx.guild,
            "_message": ctx.message,
            **globals(),
        }

        err = out = None

        try:
            exec(
                f'async def _execute_human():\n{textwrap.indent(cleanup_code(code), "  ")}',
                vars,
            )
        except Exception as e:
            err = await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
            return await ctx.message.add_reaction(self.no)

        try:
            with contextlib.redirect_stdout(io.StringIO()):
                var = await vars["_execute_human"]()
        except Exception:
            value = io.StringIO().getvalue()
            err = await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = io.StringIO().getvalue()
            if var is None:
                if value:
                    try:

                        out = await ctx.send(f"```py\n{value}\n```")
                    except Exception:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f"```py\n{page}\n```")
                                break
                            await ctx.send(f"```py\n{page}\n```")

            else:
                try:
                    out = await ctx.send(f"```py\n{value}{var}\n```")
                except Exception:
                    paginated_text = paginate(f"{value}{var}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")

        if out:
            await ctx.message.add_reaction(self.yes)
        elif err:
            await ctx.message.add_reaction(self.no)
        else:
            await ctx.message.add_reaction(self.yes)

    @commands.command(aliases=["rs"])
    async def restart(self, ctx: commands.Context) -> None:
        await self.restart_bot(ctx)

    @commands.command(name="eval", aliases=["e"])
    async def _eval(self, ctx: commands.Context, *, code: str):

        """Evaluates python code."""

        await self._execute_children(ctx, code)

    @commands.command()
    @commands.is_owner()
    async def toggle(self, ctx: commands.Context, command: str):
        await ctx.message.add_reaction("✅")

        cmd = self.bot.get_command(command.lower())

        if cmd.enabled:
            cmd.enabled = False
            return

        cmd.enabled = True


def setup(bot):
    bot.add_cog(Owner(bot))
