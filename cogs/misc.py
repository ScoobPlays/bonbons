import disnake
from disnake.ext import commands
import base64
import aiohttp


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def encode(self, ctx, *, text):
        message_bytes = text.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        embed = disnake.Embed(
            title="✅ Message Was Encoded", color=disnake.Color.green()
        )
        embed.add_field(name="Output:", value=base64_message)
        await ctx.send(embed=embed)

    @encode.error
    async def encode_error(self, ctx, error):
        embed = disnake.Embed(
            title="Encoding Error", description="Sorry, I couldn't encode that message."
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def decode(self, ctx, *, text):
        base64_bytes = text.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode("ascii")
        embed = disnake.Embed(
            title="✅ Message Was Encoded", color=disnake.Color.green()
        )
        embed.add_field(name="Output:", value=message)
        await ctx.send(embed=embed)

    @decode.error
    async def decode_error(self, ctx, error):
        embed = disnake.Embed(
            title="Decoding Error", description="Sorry, I couldn't decode that message."
        )
        await ctx.send(embed=embed)

    @commands.command(help="Says whatever you want for you!")
    async def say(self, ctx, *, message):
        await ctx.send(message)

    @commands.slash_command()
    async def say(self, inter, message):
        await inter.response.send_message(message)

    """Animals"""

    @commands.command()
    async def cat(self, ctx):
        """Sends a random cat image"""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = disnake.Embed().set_image(url=js["file"])
                    await ctx.send(embed=embed)

    @commands.slash_command()
    async def cat(self, inter):
        """Sends a random cat image"""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = disnake.Embed().set_image(url=js["file"])
                    await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command()
    async def dog(self, ctx):
        """Sends a random dog image"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = disnake.Embed().set_image(url=js["message"])
                    await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, inter):
        """Sends a random dog image"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = disnake.Embed().set_image(url=js["message"])
                    await inter.response.send_message(embed=embed, ephemeral=False)


def setup(bot):
    bot.add_cog(Misc(bot))
