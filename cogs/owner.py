import disnake
from disnake.ext import commands
import io
import textwrap
import traceback
from contextlib import redirect_stdout
from utils.utils import restart_bot, cleanup_code, paginate


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("rs",))
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        try:
            embed = disnake.Embed(
                description="Restarting the bot.", color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            print("Restarting...")
            restart_bot()
        except Exception:
            await ctx.send("Couldn't restart the bot.")

    @commands.command(
        name="eval", aliases=["e"]
    )  # totally didnt steal this from somewhere
    async def _eval(self, ctx, *, code):
        """Evaluates python code."""
        env = {
            "ctx": ctx,
            "bot": self.bot,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
        }

        env.update(globals())

        code = cleanup_code(code)
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
            with redirect_stdout(stdout):
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
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f"```py\n{page}\n```")
                                break
                            await ctx.send(f"```py\n{page}\n```")
            else:
                try:
                    out = await ctx.send(f"```py\n{value}{ret}\n```")
                except Exception:
                    paginated_text = paginate(f"{value}{ret}")
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


def setup(bot):
    bot.add_cog(Owner(bot))
