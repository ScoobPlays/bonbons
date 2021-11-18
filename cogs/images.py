from disnake import Embed, Color, ApplicationCommandInteraction
from disnake.ext import commands
from aiohttp import ClientSession


class Images(commands.Cog, description="Image related commands."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cat")
    async def cat(self, ctx: commands.Context):
        """Sends a random cat image"""
        async with ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    data = await r.json()
                    await ctx.send(
                        embed=Embed(color=Color.greyple()).set_image(url=data["file"])
                    )

    @commands.slash_command(name="cat")
    async def cat_slash(self, inter: ApplicationCommandInteraction):
        """Sends a random cat image"""
        async with ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    data = await r.json()
                    await inter.response.send_message(
                        embed=Embed(color=Color.greyple()).set_image(url=data["file"]),
                        ephemeral=False,
                    )

    @commands.command(name="dog")
    async def dog(self, ctx: commands.Context):
        """Sends a random dog image"""
        async with ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                if r.status == 200:
                    data = await r.json()
                    await ctx.send(
                        embed=Embed(color=Color.greyple()).set_image(
                            url=data["message"]
                        )
                    )

    @commands.slash_command(name="dog")
    async def dog_slash(self, inter: ApplicationCommandInteraction):
        """Sends a random dog image"""
        async with ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                if r.status == 200:
                    data = await r.json()

                    await inter.response.send_message(
                        embed=Embed(color=Color.greyple()).set_image(
                            url=data["message"]
                        ),
                        ephemeral=False,
                    )


def setup(bot):
    bot.add_cog(Images(bot))
