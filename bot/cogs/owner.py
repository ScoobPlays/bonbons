import contextlib
import io
import textwrap
import traceback

import disnake
from disnake.ext import commands
from utils.objects import cleanup_code
from utils.paginators import TextPaginator


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> int:
        return ctx.author.id == 656073353215344650

    @commands.command(name="eval", aliases=["e"])
    async def _eval(self, ctx: commands.Context, *, code: str):

        variables: dict = {
            "ctx": ctx,
            "bot": self.bot,
            "disnake": disnake,
            "discord": disnake,
            "_channel": ctx.channel,
            "_author": ctx.author,
            "_guild": ctx.guild,
            "_message": ctx.message,
            "nl": "\n",
            **globals(),
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

        if result == "None":
            return

        embed = disnake.Embed(
            description=f"```py\n{result}\n```", color=disnake.Color.blurple()
        )
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        context = await self.bot.get_context(after)
                
        if after.content.startswith((f'{context.prefix}e', f'{context.prefix}eval')):
            await self.bot.process_commands(after)


def setup(bot):
    bot.add_cog(Owner(bot))
