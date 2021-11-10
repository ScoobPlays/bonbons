import disnake
from disnake.ext import commands

"""[WIP]"""

class Threads(commands.Cog, description="Thread related commands."):
    def __init__(self, bot):
        self.bot=bot

    @commands.group()
    async def thread(self, ctx):
        """Thread related commands."""
        pass

    @thread.command()
    async def find(self, ctx, *, argument: str):
        """Finds the guild for a thread."""
        try:
            amount = []
            for channel in ctx.guild.text_channels:
                for thread in channel.threads:
                    if thread.name.startswith(argument) or thread.name == argument:
                        amount.append(thread.mention)
            await ctx.send(", ".join(amount))
        except Exception:
            await ctx.send(embed=disnake.Embed(description=f"There were no threads called or started with \"**{argument}**\".", color=disnake.Color.red()))

    @thread.command()
    @commands.has_permissions(manage_channels=True)
    async def massdelete(self, ctx):
        """Deletes every thread on the guild."""
        for channel in ctx.guild.text_channels:
            for thread in channel.threads:
                await thread.delete()
                await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(Threads(bot))