import disnake
from disnake.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: str):

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=disnake.Embed(
                    title="Missing Required Argument",
                    description=error,
                    color=disnake.Color.red(),
                )
                )

        elif isinstance(error, disnake.Forbidden):
            await ctx.send(
                embed=disnake.Embed(
                    description="I do not have enough permissions to invoke this command.",
                    color=disnake.Color.red()
                )
            )

        else:
            await ctx.reply(
                embed=disnake.Embed(description=error, color=disnake.Color.red())
            )
            raise error

def setup(bot):
    bot.add_cog(Errors(bot))
