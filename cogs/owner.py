import disnake
from disnake.ext import commands
import os
import sys

def restart_bot():
    os.execv(sys.executable, ["python"] + sys.argv)


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="restart",
        aliases=(
            "rs",
            "shutdown",
        ),
    )
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        try:
            embed = disnake.Embed(description="Restarting the bot.", color=disnake.Color.red())
            await ctx.send(embed=embed)
            print("Restarting...")
            restart_bot()
        except Exception:
            await ctx.send("Couldn't restart the bot.")

def setup(bot):
    bot.add_cog(Owner(bot))
