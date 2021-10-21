import disnake
from disnake.ext import commands
import base64
import aiohttp
from urllib.parse import quote_plus


class Google(disnake.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"
        self.add_item(disnake.ui.Button(label="Click Here", url=url))


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def encode(self, ctx: commands.Context, *, body:str):
        message_bytes = body.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        embed = disnake.Embed(
            title="✅ Message Was Encoded", color=disnake.Color.green()
        )
        embed.add_field(name="Output:", value=base64_message)
        await ctx.send(embed=embed)

    @encode.error
    async def encode_error(self, ctx: commands.Context, error):
        embed = disnake.Embed(
            title="Encoding Error", description="Sorry, I couldn't encode that message."
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def decode(self, ctx: commands.Context, *, body:str):
        base64_bytes = body.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode("ascii")
        embed = disnake.Embed(
            title="✅ Message Was Encoded", color=disnake.Color.green()
        )
        embed.add_field(name="Output:", value=message)
        await ctx.send(embed=embed)

    @decode.error
    async def decode_error(self, ctx: commands.Context, error):
        embed = disnake.Embed(
            title="Decoding Error", description="Sorry, I couldn't decode that message."
        )
        await ctx.send(embed=embed)

    @commands.command(name="say", help="Says whatever you want for you!")
    async def say_cmd(self, ctx: commands.Context, *, message:str):
        await ctx.send(message)

    @commands.slash_command(name="say")
    async def say_slash(self, inter: disnake.ApplicationCommandInteraction, message:str):
        "Says whatever you want for you!"
        await inter.response.send_message(message, ephemeral=False)

    """Animals"""

    @commands.command(name="cat")
    async def cat_cmd(self, ctx: commands.Context):
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
    async def dog_cmd(self, ctx: commands.Context):
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
    async def google_cmd(self, ctx: commands.Context, *, query: str):
        """Returns a google link for a query."""
        await ctx.send(f"Google Result for: `{query}`", view=Google(query))

    @commands.slash_command(name="google")
    async def google_slash(self, inter: disnake.ApplicationCommandInteraction, query: str):
        """Returns a google link for a query."""
        await inter.response.send_message(
            f"Google Result for: `{query}`", view=Google(query), ephemeral=False
        )


def setup(bot):
    bot.add_cog(Misc(bot))
