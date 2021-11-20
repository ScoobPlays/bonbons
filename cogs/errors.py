import disnake
from disnake.ext.commands import Cog, Context, CommandNotFound, MissingRequiredArgument

class Errors(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: str):

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, CommandNotFound):
            return

        elif isinstance(error, MissingRequiredArgument):
            await ctx.reply(
                embed=disnake.Embed(
                    title="Missing Required Argument",
                    description=error,
                    color=disnake.Color.red(),
                ),
                mention_author=False,
            )

        else:
            await ctx.reply(
                embed=disnake.Embed(
                    description=error,
                    color=disnake.Color.red()
                )
            )
            raise error

def setup(bot):
    bot.add_cog(Errors(bot))
