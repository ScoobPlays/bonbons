import disnake
from disnake.ext import commands

class Threads(commands.Cog, description="Thread related commands."):
    def __init__(self, bot):
        self.bot=bot

    @commands.group()
    async def thread(self, ctx):
        pass

    @thread.command()
    async def find(self, ctx, *, argument: str):
        try:
            amount = []
            for channel in ctx.guild.text_channels:
                for thread in channel.threads:
                    if thread.name.startswith(argument) or thread.name == argument:
                        amount.append(thread.mention)
            await ctx.send(", ".join(amount))
        except Exception:
            await ctx.send(f"There were no threads called or started with \"**{argument}**\".")

    @thread.command()
    @commands.has_permissions(manage_channels=True)
    async def massdelete(self, ctx):
        for channel in ctx.guild.text_channels:
            for thread in channel.threads:
                await thread.delete()
                await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(Threads(bot))