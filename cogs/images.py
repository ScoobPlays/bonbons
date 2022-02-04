import io

import disnake
from disnake.ext import commands
from easy_pil import Canvas, Editor, Font


class Images(commands.Cog):
    """Image manipulation related commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emoji = "🖼️"

    @commands.command()
    async def text(self, ctx: commands.Context, *, text: str):
        """Sends an image with text."""
        image = Editor(Canvas((800, 280), color="#00000000"))
        image.text((100, 100), text, font=Font.poppins(size=50), color="white")

        with io.BytesIO() as bytes:
            image.save(bytes, "PNG")
            bytes.seek(0)
            await ctx.send(file=disnake.File(fp=bytes, filename="text.png"))


def setup(bot):
    bot.add_cog(Images(bot))
