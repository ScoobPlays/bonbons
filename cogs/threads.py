from disnake import (
    Embed,
    Color
)
from disnake.ext import commands


class Threads(commands.Cog, description="Thread utilities."):
    def __init__(self, bot):
        self.bot = bot

    async def find_thread(ctx, name):
        try:
            threads = []
            for channel in ctx.guild.text_channels:
                for thread in channel.threads:
                    if thread.name.startswith(name) or thread.name == name:
                        threads.append(thread.mention)
            await ctx.send(", ".join(threads))
        except Exception:
            await ctx.send(
                embed=Embed(
                    description=f'No threads were found.',
                    color=Color.red(),
                )
            )

    @commands.group()
    async def thread(self, ctx: commands.Context):
        """Base command for thread."""
        pass

    @thread.command()
    async def find(self, ctx: commands.Context, *, name: str):

        """Searches the guild for a thread."""
        
        await self.find_thread(ctx, name)


    @thread.command()
    @commands.has_permissions(manage_channels=True)
    async def massdelete(self, ctx: commands.Context):
        """Deletes every thread in the guild."""
        for channel in ctx.guild.text_channels:
            for thread in channel.threads:
                await thread.delete()
                await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Threads(bot))
