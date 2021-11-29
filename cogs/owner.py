import io, os, sys, textwrap, traceback, contextlib
from disnake.ext import commands
from together import *
import disnake

class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

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
            await ctx.send(
                embed=disnake.Embed(
                    description="Restarting the bot.", color=disnake.Color.greyple()
                )
            )
            os.execv(sys.executable, ["python"] + sys.argv)
        except Exception:
            await ctx.send(
                embed=disnake.Embed(
                    description="Bot failed to restart.", color=disnake.Color.red()
                )
            )

    async def eval_code(self, ctx: commands.Context, code: str) -> str:
        env = {
            "ctx": ctx,
            "bot": self.bot,
            "channel": ctx.channel,
            "_channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "_guild": ctx.guild,
            "message": ctx.message,
            "_message": ctx.message,
            "msg": ctx.message,
            "_msg": ctx.message,
            "_find": disnake.utils.find,
            "_get": disnake.utils.get,
        }

        env.update(globals())

        code = self.cleanup_code(code)
        stdout = io.StringIO()
        err = out = None
        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
            return await ctx.message.add_reaction("\u2049")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            err = await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            if ret is None:
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
                    out = await ctx.send(f"```py\n{value}{ret}\n```")
                except Exception:
                    paginated_text = self.paginate(f"{value}{ret}")
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
    @commands.is_owner()
    async def restart(self, ctx: commands.Context) -> None:
        await self.restart_bot(ctx)

    @commands.command(name="eval", aliases=["e"])
    @commands.is_owner()
    async def _eval(self, ctx: commands.Context, *, code: str) -> str:

        """Evaluates python code."""

        await self.eval_code(ctx, code)


def setup(bot):
    bot.add_cog(Owner(bot))
