import disnake
from disnake.ext import commands
import aiohttp


class Images(commands.Cog, description="Image related commands."):
    def __init__(self, bot):
        self.bot = bot

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


def setup(bot):
    bot.add_cog(Images(bot))
