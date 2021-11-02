import disnake
from disnake.ext import commands
import aiohttp
from urllib.parse import quote_plus


class Google(disnake.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"
        self.add_item(disnake.ui.Button(label="Click Here", url=url))


class Misc(commands.Cog, description="Very weird commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say", help="Says whatever you want for you")
    async def say(self, ctx: commands.Context, *, argument: str):
        await ctx.send(argument)

    @commands.slash_command(name="say")
    async def say_slash(
        self, inter: disnake.ApplicationCommandInteraction, argument: str
    ):
        "Says whatever you want for you"
        await inter.response.send_message(argument, ephemeral=False)

    """Animals"""

    @commands.command(name="cat")
    async def cat(self, ctx: commands.Context):
        """Sends a random cat image"""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = disnake.Embed().set_image(url=js["file"])
                    await ctx.send(embed=embed)

    @commands.slash_command(name="cat")
    async def cat_slash(self, inter: disnake.ApplicationCommandInteraction):
        """Sends a random cat image"""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = disnake.Embed().set_image(url=js["file"])
                    await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="dog")
    async def dog(self, ctx: commands.Context):
        """Sends a random dog image"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = disnake.Embed().set_image(url=js["message"])
                    await ctx.send(embed=embed)

    @commands.slash_command(name="dog")
    async def dog_slash(self, inter: disnake.ApplicationCommandInteraction):
        """Sends a random dog image"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = disnake.Embed().set_image(url=js["message"])
                    await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="google")
    async def google(self, ctx: commands.Context, *, query: str):

        """Returns a google link for a query"""

        await ctx.send(f"Google Result for: `{query}`", view=Google(query))

    @commands.slash_command(name="google")
    async def google_slash(
        self, inter: disnake.ApplicationCommandInteraction, query: str
    ):
        """Returns a google link for a query"""

        await inter.response.send_message(
            f"Google Result for: `{query}`", view=Google(query), ephemeral=False
        )


def setup(bot):
    bot.add_cog(Misc(bot))
