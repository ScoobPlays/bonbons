from datetime import datetime
import disnake
from disnake.ext import commands
import aiohttp


class Fun(commands.Cog, description="Very unuseful commands"):
    def __init__(self, bot):
        self.bot = bot
        self.last_msg = None

    @commands.Cog.listener()
    async def on_message_delete(
        self, message: disnake.Message
    ):  # on msg delete for snipe command
        self.last_msg = message

    @commands.command(help="Snipes the most recently deleted message.")
    async def snipe(self, ctx):
        if self.last_msg.guild.id == ctx.guild.id:

            embed = disnake.Embed(description=f"{self.last_msg.content}")
            embed.set_footer(text=f"Message from {self.last_msg.author}")
            embed.set_author(
                name=f"{self.last_msg.author}",
                icon_url=self.last_msg.author.display_avatar,
            )
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

        else:
            embed = disnake.Embed(
                title="Error",
                description="Sorry, I couldn't find the most recently deleted message.",
            )
            embed.timestamp = datetime.utcnow()
            embed.set_footer(name=ctx.author, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embed)

    @commands.command(help="Generates a random token")
    async def token(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/bottoken") as r:
                data = await r.json()
                await ctx.reply(f'Here\'s your token: `{data["token"]}`')

    @commands.command(help="Gives a joke")
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/joke") as r:
                data = await r.json()
                await ctx.send(data["joke"])


def setup(bot):
    bot.add_cog(Fun(bot))

