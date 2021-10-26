import disnake
from disnake.ext import commands
import os
import sys


def restart_bot():
    os.execv(sys.executable, ["python"] + sys.argv)


class Owner(commands.Cog):
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
    async def restart_cmd(self, ctx):
        try:
            embed = disnake.Embed(title="Restarting...", color=disnake.Color.red())
            await ctx.send(embed=embed)
            print("Restarting...")
            restart_bot()
        except Exception:
            await ctx.send("Couldn't restart the bot.")

    @commands.slash_command(name="restart")
    @commands.is_owner()
    async def restart_slash(self, inter):
        """Restarts the bot"""
        try:
            embed = disnake.Embed(title="Restarting...", color=disnake.Color.red())
            await inter.response.send_message(embed=embed)
            print("Restarting...")
            restart_bot()
        except Exception as e:
            await inter.response.send_message("Couldn't restart the bot.")
            print(e)


def setup(bot):
    bot.add_cog(Owner(bot))
