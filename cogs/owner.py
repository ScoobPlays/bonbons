import discord
from discord.ext import commands
import os
import sys
from datetime import datetime
import platform
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout

hm = datetime.utcnow()


def restart_bot():
    os.execv(sys.executable, ["python"] + sys.argv)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rs", "shutdown"])
    @commands.is_owner()
    async def restart(self, ctx):
        embed = discord.Embed(title="Restarting...", color=discord.Color.red())
        await ctx.send(embed=embed)
        print("Restarting...")
        restart_bot()

    @commands.command()
    @commands.is_owner()
    async def stats(self, ctx):

        delta_uptime = datetime.utcnow() - hm
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        embed = discord.Embed(title="Bot Information")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/888309915620372491/ee8c4ed341cb7cb954eefc7f08b879ec.png?size=1024"
        )
        embed.add_field(
            name="Statistics",
            value=f"• Ping: {round(self.bot.latency * 1000)}ms\n• Uptime: {hours}h, {minutes}m, {seconds}s\n• Servers: {len(self.bot.guilds)}\n• Users: {len(self.bot.users)}\n• PyVersion: {platform.python_version()}",
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help Page", color=discord.Color.green())
        embed.add_field(
            name="Main", value="`kiss`, `bonk`, `spank`, `slap`, `wink`, `pat`, `hug`"
        )
        embed.add_field(
            name="Misc",
            value="`say`, `luck`, `encode`, `decode`, `wiki`, `mincraft`, `dog`, `cat`, `snipe`, `color`, `token`, `joke`",
        )
        embed.add_field(
            name="Information",
            value="`membercount`, `userinfo`, `serverinfo`, `roleinfo`, `spotify`, `avatar`",
        )
        embed.add_field(
            name="Utility", value="`ping`, `nick`, `massnick`, `ban`, `unban`, `clean`"
        )
        embed.timestamp = datetime.utcnow()
        embed.set_footer(
            text=f"Commands: {len(self.bot.commands)}",
            icon_url=ctx.author.display_avatar,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="eval"
    )  # not my evaluate command nor do I claim it is mine. i forgot where I got it though.. :(
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        """Evaluates python code."""
        env = {
            "ctx": ctx,
            "bot": self.bot,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
        }

        def cleanup_code(content):
            """Automatically removes code blocks from the code."""
            if content.startswith("```") and content.endswith("```"):
                return "\n".join(content.split("\n")[1:-1])

            return content.strip("` \n")

        def get_syntax_error(e):
            if e.text is None:
                return f"```py\n{e.__class__.__name__}: {e}\n```"
            return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

        env.update(globals())

        code = cleanup_code(code)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'

        def paginate(text: str):
            """Simple generator that paginates text."""
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
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f"```py\n{page}\n```")
                                break
                            await ctx.send(f"```py\n{page}\n```")
            else:
                try:
                    out = await ctx.send(f"```py\n{value}{ret}\n```")
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")

        if out:
            await ctx.message.add_reaction("\u2705")  # tick
        elif err:
            await ctx.message.add_reaction("\u2049")  # x=
        else:
            await ctx.message.add_reaction("\u2705")


def setup(bot):
    bot.add_cog(Owner(bot))
