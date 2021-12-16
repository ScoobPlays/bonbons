import disnake
from disnake.ext import commands


class NSFW(commands.Cog, description="NSFW commands."):
    def __init__(self, bot):
        self.bot = bot

    async def get_img(self, imgtype: str):
        async with self.bot.session.get(
            f"https://nekobot.xyz/api/image?type={imgtype}"
        ) as res:
            res = await res.json()
        return res.get("message")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ass(self, ctx):
        """Posts a random ass image."""
        if not ctx.channel.is_nsfw():
            await ctx.send("This command can only be used in an NSFW channel.")
            return

        image = await self.get_img("ass")
        em = disnake.Embed(color=ctx.author.color)
        em.set_image(url=image)

        await ctx.send(embed=em)

    @commands.command(name="4k")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _4k(self, ctx):

        """Posts a random 4k image."""

        if not ctx.channel.is_nsfw():
            await ctx.send("This command can only be used in an NSFW channel.")
            return

        image = await self.get_img("4k")
        em = disnake.Embed(color=ctx.author.color)
        em.set_image(url=image)

        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pgif(self, ctx):

        """Posts a random NSFW image/gif."""

        if not ctx.channel.is_nsfw():
            await ctx.send("This command can only be used in an NSFW channel.")
            return

        image = await self.get_img("pgif")
        em = disnake.Embed(color=ctx.author.color)
        em.set_image(url=image)

        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pussy(self, ctx):

        """Posts a random pussy image/gif."""

        if not ctx.channel.is_nsfw():
            await ctx.send("This command can only be used in an NSFW channel.")
            return

        image = await self.get_img("pussy")
        em = disnake.Embed(color=ctx.author.color)
        em.set_image(url=image)

        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hentai(self, ctx):

        """Posts a random hentai image/gif."""

        if not ctx.channel.is_nsfw():
            return await ctx.send("This command can only be used in an NSFW channel.")

        image = await self.get_img("hentai")
        em = disnake.Embed(color=ctx.author.color)
        em.set_image(url=image)

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(NSFW(bot))
