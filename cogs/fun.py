from datetime import datetime
import disnake
from disnake.ext import commands
import random
import aiohttp


class Fun(commands.Cog):
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

    @commands.command()
    async def luck(self, ctx, *, lucky_on):
        randome = random.randint(0, 100)

        random_day = [
            "tomorrow is",
            "next week is",
            "this Friday is",
            "this Monday is",
            "next year is",
            "in 2050 is",
        ]
        rng_day = random.choice(random_day)

        embed = disnake.Embed(
            description=f"Your luck of getting **{lucky_on}** {rng_day} **{randome}**%",
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(help="Generates a random token.")
    async def token(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/bottoken") as r:
                data = await r.json()
                await ctx.send(f'Here\'s your token: `{data["token"]}`')

    @commands.command(help="Gives a joke!")
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/joke") as r:
                data = await r.json()
                await ctx.send(data["joke"])


def setup(bot):
    bot.add_cog(Fun(bot))
