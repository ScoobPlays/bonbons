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
                embed=disnake.Embed(description=error, color=disnake.Color.red())
            )
            raise error

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: disnake.ApplicationCommandInteraction, error: str
    ):

        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message(
                embed=disnake.Embed(
                    description="Missing permissions",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )

        else:
            await inter.response.send_message(
                embed=disnake.Embed(description=error, color=disnake.Color.red()),
                ephemeral=True,
            )
            raise error


def setup(bot):
    bot.add_cog(Errors(bot))
