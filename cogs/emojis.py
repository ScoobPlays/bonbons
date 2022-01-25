from disnake.ext import commands
from utils.replies import REPLIES
import random
import disnake


class Emojis(commands.Cog):
    """A collection of commands for discord emojis."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "😃"

    async def send_error_message(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=random.choice(REPLIES),
            description="Something went wrong.",
            color=disnake.Color.red(),
        )
        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name="emoji")
    async def emoji(self, ctx):
        pass

    @emoji.sub_command()
    @commands.has_permissions(manage_emojis=True)
    async def copy(
        self,
        inter,
        emoji: str = commands.Param(
            description="The emoji object, must be a valid emoji, or it's ID."
        ),
        name: str = commands.Param(
            description="The emoji name, defaults to emoji is no name was given."
        ),
    ):

        """
        Copies an emoji. Could be <:name:id> or the emoji ID itself.
        """

        name = name or "emoji"

        if type(emoji) == int:
            valid_emoji = emoji

        if type(emoji) == str:
            invalid_emoji = emoji.split(":")
            valid_emoji = invalid_emoji[2].replace(">", "").replace("<", "")

        try:
            async with self.bot.session.get(
                f"https://cdn.discordapp.com/emojis/{valid_emoji}.png?size=80"
            ) as data:
                emoji = await data.read()
                emote = await inter.guild.create_custom_emoji(name=name, image=emoji)
                await inter.response.send_message(emote)
        except Exception as e:
            print(e)
            await self.send_error_message(inter)

    @emoji.sub_command()
    @commands.has_permissions(manage_emojis=True)
    async def create(
        self,
        inter,
        url: str = commands.Param(description="A valid url of sort."),
        name: str = commands.Param(
            description="The emoji name, defaults to emoji if no name was given."
        ),
    ):
        """
        Creates an emoji via link.
        """
        name = name or "emoji"

        try:
            async with self.bot.session.get(url) as data:
                emoji = await data.read()
                emote = await inter.guild.create_custom_emoji(name=name, image=emoji)
                await inter.response.send_message(emote, ephemeral=True)
        except Exception as e:
            print(e)
            await self.send_error_message(inter)

    @emoji.sub_command()
    @commands.has_permissions(manage_emojis=True)
    async def delete(
        self,
        inter,
        emoji: disnake.Emoji = commands.Param(
            description="The emoji object, must be the emoji itself, or it's ID."
        ),
    ):
        """
        Deletes an emoji via the emoji itself, or the emoji ID.
        """

        if type(emoji) == disnake.Emoji:
            await emoji.delete()
            await inter.response.send_message("Success!")

        else:
            await self.send_error_message(inter)


def setup(bot):
    bot.add_cog(Emojis(bot))
