from disnake.ext import commands
import utils
import disnake
import io
import os
import sys
import textwrap
import traceback
import contextlib


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> int:
        return ctx.author.id == 656073353215344650

    def paginate(self, text: str) -> str:
        last = 0
        pages = []

        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr

            if appd_index != len(text) - 1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != "", pages))

    def cleanup_code(self, content: str) -> str:
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

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

    async def run(self, ctx: commands.Context, code: str):
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
                f'async def evaluate():\n{textwrap.indent(self.cleanup_code(code), "  ")}',
                vars,
            )
        except Exception as e:
            err = await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
            return await ctx.message.add_reaction("\u2049")

        try:
            with contextlib.redirect_stdout(io.StringIO()):
                var = await vars["evaluate"]()
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
                        paginated_text = self.paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f"```py\n{page}\n```")
                                break
                            await ctx.send(f"```py\n{page}\n```")
            else:
                try:
                    out = await ctx.send(f"```py\n{value}{var}\n```")
                except Exception:
                    paginated_text = self.paginate(f"{value}{var}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")

        if out:
            await ctx.message.add_reaction("\u2705")
        elif err:
            await ctx.message.add_reaction("\u2049")
        else:
            await ctx.message.add_reaction("\u2705")

    @commands.command(aliases=("rs",))
    async def restart(self, ctx: commands.Context) -> None:
        await self.restart_bot(ctx)

    @commands.command(name="eval", aliases=("e",))
    async def _eval(self, ctx: commands.Context, *, code: str) -> str:

        """Evaluates python code."""

        await self.run(ctx, code)

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
