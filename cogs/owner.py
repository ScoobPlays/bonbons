import disnake
from disnake.ext import commands
import os
import sys


def restart_bot():
    os.execv(sys.executable, ["python"] + sys.argv)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("rs", "shutdown",))
    @commands.is_owner()
    async def restart(self, ctx):
        embed = disnake.Embed(title="Restarting...", color=disnake.Color.red())
        await ctx.send(embed=embed)
        print("Restarting...")
        restart_bot()


def setup(bot):
    bot.add_cog(Owner(bot))
