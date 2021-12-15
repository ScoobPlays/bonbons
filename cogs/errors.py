import disnake
from disnake.ext import commands


def human_join(seq, delim=", ", final="or"):
    size = len(seq)
    if size == 0:
        return ""

    if size == 1:
        return seq[0]

    if size == 2:
        return f"{seq[0]} {final} {seq[1]}"

    return delim.join(seq[:-1]) + f" {final} {seq[-1]}"


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
            _missing_args = list(ctx.command.clean_params)
            missing_args = [
                f"`{arg}`"
                for arg in _missing_args[_missing_args.index(error.param.name) :]
            ]
            return await ctx.send(
                f'You are missing the following required arguments: {human_join(missing_args, final="and")}'
            )

        elif isinstance(error, disnake.Forbidden):
            await ctx.send(error)

        else:
            await ctx.reply(error)
            raise error


def setup(bot):
    bot.add_cog(Errors(bot))
