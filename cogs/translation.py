from disnake.ext import commands
from utils.translation import b64_encode, b64_decode


class Translation(
    commands.Cog,
    description="Commands that can translate something into another language",
):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def base64(self, inter):
        pass

    @base64.sub_command()
    async def encode(self, inter, text: str):
        """Encodes a message into a base64 string"""
        try:
            await inter.response.send_message(b64_encode(text), ephemeral=False)
        except Exception:
            await inter.response.send_message(
                f"Couldn't encode that message.", ephemeral=False
            )

    @base64.sub_command()
    async def decode(self, inter, text: str):
        """Decodes a base64 string"""
        try:
            await inter.response.send_message(b64_decode(text), ephemeral=False)
        except Exception:
            await inter.response.send_message(
                "Couldn't decode that message.", ephemeral=False
            )


def setup(bot):
    bot.add_cog(Translation(bot))
