import disnake
from disnake.ext import commands


class Utilities(commands.Cog, description="Commands for the bot."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def suggest(self, ctx: commands.Context, *, suggestion: str):
        """Suggest a feature to the bot."""
        try:
            suggestions = self.bot.get_channel(908905706055405618)

            msg = await suggestions.send(
                embed=disnake.Embed(
                    title=f"Suggestion by {ctx.author}",
                    description=suggestion,
                    color=disnake.Color.greyple(),
                )
            )
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        except Exception as e:
            await ctx.send(
                embed=disnake.Embed(description=e, color=disnake.Color.red())
            )


def setup(bot):
    bot.add_cog(Utilities(bot))
