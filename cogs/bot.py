import disnake
import utils
from disnake.ext import commands


class Bot(commands.Cog, description="Commands for the bot."):
    def __init__(self, bot):
        self.bot = bot
        self.db = utils.db["bot"]

    @commands.command(
        aliases=(
            "uptime",
            "botinfo",
        )
    )
    async def info(self, ctx):
        """Returns the bots info."""
        embed = disnake.Embed(
            title="My Information",
            color=disnake.Color.greyple(),
            description=f"I have access to {len(self.bot.guilds)} guilds and can see {len(self.bot.users)} users. ",
        )

        data = await self.db.find_one({"_id": self.bot.user.id})
        embed.add_field(
            name="Commands", value=f"**{data['uses']}** commands have been invoked."
        )
        embed.add_field(
            name="Uptime",
            value=f"I have been online since <t:{int(self.bot.uptime)}:R>",
            inline=False,
        )
        await ctx.send(embed=embed, view=utils.Advertising())


def setup(bot):
    bot.add_cog(Bot(bot))
