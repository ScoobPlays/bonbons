from disnake.ext.commands import Cog, Context, Bot, group, is_nsfw, command
import disnake

BASE_URL = "https://api.waifu.im"


class NotSafeForWork(Cog, description="NSFW related commands."):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.emoji = "🔞"

    async def _get_image(self, ctx: Context, type: str, *, gif: bool = False):
        if gif:
            url = f"{BASE_URL}/nsfw/{type}/?gif=True"
        else:
            url = f"{BASE_URL}/nsfw/{type}/"

        async with self.bot.session.get(url) as response:
            base = (await response.json())["images"][0]

            return (
                disnake.Embed(color=disnake.Color.blurple())
                .set_author(
                    name=str(ctx.author),
                    icon_url=ctx.author.display_avatar,
                    url=base["source"],
                )
                .set_image(url=base["url"])
            )

    async def _get_sfw_image(self, ctx: Context, type: str):

        async with self.bot.session.get(f"{BASE_URL}/sfw/{type}/") as response:
            base = (await response.json())["images"][0]

            return (
                disnake.Embed(color=disnake.Color.blurple())
                .set_author(
                    name=str(ctx.author),
                    icon_url=ctx.author.display_avatar,
                    url=base["source"],
                )
                .set_image(url=base["url"])
            )

    @group(name="nsfw", invoke_without_command=True)
    @is_nsfw()
    async def nsfw(self, ctx: Context):
        """The base command for all the NSFW commands."""
        await ctx.send_help("nsfw")

    @nsfw.command()
    async def ass(self, ctx: Context, gif: bool = False):
        """Ass focused content."""
        img = await self._get_image(ctx, "ass", gif=gif)
        await ctx.send(embed=img)

    @nsfw.command(aliases=["ero"])
    async def erotic(self, ctx: Context, gif: bool = False):
        """Erotic content."""
        img = await self._get_image(ctx, "ero", gif=gif)
        await ctx.send(embed=img)

    @nsfw.command()
    async def hentai(self, ctx: Context, gif: bool = False):
        """Any kind of erotic content."""
        img = await self._get_image(ctx, "hentai", gif=gif)
        await ctx.send(embed=img)

    @nsfw.command()
    async def maid(self, ctx: Context):
        """Sexy womans or girl employed to do domestic work in their working uniform."""
        img = await self._get_image(ctx, "maid")
        await ctx.send(embed=img)

    @nsfw.command()
    async def milf(self, ctx: Context, gif: bool = False):
        """A sexually attractive middle-aged woman."""
        img = await self._get_image(ctx, "milf", gif=gif)
        await ctx.send(embed=img)

    @nsfw.command()
    async def oppai(self, ctx: Context, gif: bool = False):
        """Boobs focused content."""
        img = await self._get_image(ctx, "oppai", gif=gif)
        await ctx.send(embed=img)

    @nsfw.command()
    async def oral(self, ctx: Context, gif: bool = False):
        """Any kind of erotic content, basically any nsfw image."""
        img = await self._get_image(ctx, "oral", gif=gif)
        await ctx.send(embed=img)

    @nsfw.command()
    async def paizuri(self, ctx: Context):
        """A category of hentai that involves breast sex, also known as titty fucking."""
        img = await self._get_image(ctx, "paizuri")
        await ctx.send(embed=img)

    @nsfw.command(aliases=["selfies"])
    async def selfie(self, ctx: Context):
        """A girl taking a lewd picture of herself."""
        img = await self._get_image(ctx, "selfies")
        await ctx.send(embed=img)

    @nsfw.command()
    async def uniform(self, ctx: Context, gif: bool = False):
        """Girls wearing any kind of uniform."""
        img = await self._get_image(ctx, "uniform", gif=gif)
        await ctx.send(embed=img)

    @nsfw.command()
    async def ecchi(self, ctx: Context):
        """Slightly explicit sexual content."""
        img = await self._get_image(ctx, "ecchi")
        await ctx.send(embed=img)

    @command()
    async def waifu(self, ctx: Context):
        img = await self._get_sfw_image(ctx, "waifu")
        await ctx.send(embed=img)


def setup(bot: Bot):
    bot.add_cog(NotSafeForWork(bot))
