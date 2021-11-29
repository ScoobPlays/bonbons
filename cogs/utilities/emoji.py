from typing import Union, Optional
from datetime import datetime
from disnake.ext import commands
import disnake


class Emojis(commands.Cog, description="Emoji utilities."):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def emoji(self, ctx):
        """The base command for emoji."""
        await ctx.send_help("emoji")

    @emoji.command()
    @commands.has_permissions(manage_emojis=True)
    async def copy(self, ctx, argument: int, name: Optional[str]):

        """
        Copies an emoji using ID.
        A command for people who don't have nitro.
        """

        name = name or "emoji"
        async with ctx.typing:
            async with self.bot.session.get(
                f"https://cdn.discordapp.com/emojis/{argument}.png?size=80"
            ) as data:
                emoji = await data.read()
                emote = await ctx.guild.create_custom_emoji(name=name, image=emoji)
                await ctx.send(emote)

    @emoji.command()
    @commands.has_permissions(manage_emojis=True)
    async def create(self, ctx, url: str, name: str):

        """
        Creates an emoji by link.
        """

        name = name or "emoji"

        async with ctx.typing:
            async with self.bot.session.get(url) as data:
                emoji = await data.read()
                emote = await ctx.guild.create_custom_emoji(name=name, image=emoji)
                await ctx.send(emote)

    @emoji.command()
    @commands.has_permissions(manage_emojis=True)
    async def delete(self, ctx, name: Union[disnake.Emoji, int]):

        """
        Deletes an emoji by ID or emote.
        """

        if name == int:
            emoji = await self.bot.get_emoji(name)
            await emoji.delete()
            await ctx.message.add_reaction("✅")

        if name == disnake.Emoji:
            await name.delete()
            await ctx.message.add_reaction("✅")

        else:
            await ctx.send("An error occurred while deleting the emoji.")

    async def context_send_emojis(self, ctx):
        all_emojis = []

        for emoji in ctx.guild.emojis:
            full_emoji = f"<:{emoji.name}:{emoji.id}>"
            all_emojis.append(full_emoji)

        embed = disnake.Embed(
            title=f"Total Emoji's [{len(ctx.guild.emojis)}]",
            description="".join(all_emojis),
            color=disnake.Color.greyple(),
            timestamp=datetime.utcnow(),
        )

        if len(embed) > 2000:
            return await ctx.send("There were too many emoji's. Embed failed to send.")
        await ctx.send(embed=embed)

    async def interaction_send_emojis(self, inter):
        all_emojis = []

        for emoji in inter.guild.emojis:
            full_emoji = f"<:{emoji.name}:{emoji.id}>"
            all_emojis.append(full_emoji)

        embed = disnake.Embed(
            title=f"Total Emoji's [{len(inter.guild.emojis)}]",
            description="".join(all_emojis),
            color=disnake.Color.greyple(),
            timestamp=datetime.utcnow(),
        )

        if len(embed) > 2000:
            return await inter.response.send_message(
                "There were too many emoji's. Embed failed to send.", ephemeral=True
            )
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command()
    @commands.guild_only()
    async def emojis(self, ctx):
        """Returns all the emojis in the guild."""
        await self.context_send_emojis(ctx)

    @commands.slash_command(name="emojis")
    @commands.guild_only()
    async def emojis_slash(self, inter):
        """Returns all the emojis in the guild"""

        await self.context_send_emojis(inter)


def setup(bot):
    bot.add_cog(Emojis(bot))
