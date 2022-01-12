from typing import Union, Optional
from disnake.ext import commands
import disnake
import random

facepalms = ("🤦‍♂️", "🤦‍♀️", "🤦")


class Utilities(commands.Cog, description="Thread and emoji utilities."):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "⚙️"
        self.thank = self.bot.mongo["discord"]["thank"]

    async def send_thank(
        self, ctx: commands.Context, member: disnake.Member, reason: str
    ):
        if member == ctx.author:
            return await ctx.send(
                embed=disnake.Embed(
                    description=f"Why do you wanna thank yourself {random.choice(facepalms)}",
                    color=disnake.Color.red(),
                )
            )

        await ctx.send(
            embed=disnake.Embed(
                description=f"You thanked {member.mention}!",
                color=disnake.Color.greyple(),
            )
        )

    @commands.group(invoke_without_command=True)
    async def thank(
        self,
        ctx: commands.Context,
        member: disnake.Member = None,
        *,
        reason: Optional[str],
    ):

        """
        Thank a member for something.
        """

        if not member:
            await ctx.send_help("thank")

        else:

            await self.send_thank(ctx, member, reason)

            try:
                author = await self.thank.find_one({"_id": ctx.author.id})
                receiver = await self.thank.find_one({"_id": member.id})

                if not author:
                    await self.thank.insert_one(
                        {
                            "_id": ctx.author.id,
                            "sent": 0,
                            "received": 0,
                        }
                    )
                    new_receiver = await self.thank.find_one({"_id": ctx.author.id})

                    new_sent = new_receiver["sent"] + 1
                    await self.thank.update_one(
                        new_receiver, {"$set": {"sent": new_sent}}
                    )

                if not receiver:
                    await self.thank.insert_one(
                        {
                            "_id": member.id,
                            "sent": 0,
                            "received": 0,
                        }
                    )
                    new_find = await self.thank.find_one({"_id": member.id})

                    new_received = new_find["received"] + 1
                    await self.thank.update_one(
                        new_find, {"$set": {"received": new_received}}
                    )

                if author and receiver:
                    sent = author["sent"] + 1
                    received = receiver["received"] + 1

                await self.thank.update_one(author, {"$set": {"sent": sent}})
                await self.thank.update_one(receiver, {"$set": {"received": received}})

            except UnboundLocalError:
                return

    @thank.command(name="stats")
    async def thank_stats(self, ctx: commands.Context, member: disnake.Member = None):
        """
        Display a member's stats.
        """

        member = member or ctx.author

        data = await self.thank.find_one({"_id": member.id})

        if not data:
            return await ctx.send(
                embed=disnake.Embed(
                    description="That member does not have any stats yet.",
                    color=disnake.Color.greyple(),
                )
            )
        await ctx.send(
            embed=disnake.Embed(
                title=f"{member.display_name}'s Stats", color=disnake.Color.greyple()
            )
            .add_field(name="Thanks Sent", value=data["sent"], inline=False)
            .add_field(name="Thanks Received", value=data["received"], inline=False)
        )

    async def find_thread(self, ctx: commands.Context, name: str):
        try:
            threads = []
            for channel in ctx.guild.text_channels:
                for thread in channel.threads:
                    if thread.name.startswith(name) or thread.name == name:
                        threads.append(thread.mention)
            await ctx.send(", ".join(threads))
        except Exception:
            await ctx.send(
                "No threads were found.",
            )

    @commands.group(invoke_without_command=True)
    async def thread(self, ctx: commands.Context):
        """The base command for thread."""
        await ctx.send_help("thread")

    @thread.command()
    async def find(self, ctx: commands.Context, *, name: str):

        """Searches the current server for a thread."""

        await self.find_thread(ctx, name)

    @thread.command()
    @commands.has_permissions(manage_channels=True)
    async def massdelete(self, ctx: commands.Context):
        """Deletes every thread in the guild."""
        for channel in ctx.guild.text_channels:
            for thread in channel.threads:
                await thread.delete()
        await ctx.message.add_reaction("✅")

    @commands.group(name="emoji", invoke_without_command=True)
    async def _emoji(self, ctx: commands.Context):
        """The base command for emoji."""
        await ctx.send_help("emoji")

    @_emoji.command()
    @commands.has_permissions(manage_emojis=True)
    async def copy(self, ctx: commands.Context, argument: int, name: Optional[str]):

        """
        Copies an emoji via ID.
        """

        name = name or "emoji"
        async with ctx.typing():
            async with self.bot.session.get(
                f"https://cdn.discordapp.com/emojis/{argument}.png?size=80"
            ) as data:
                emoji = await data.read()

                emote = await ctx.guild.create_custom_emoji(name=name, image=emoji)
                await ctx.send(emote)

    @_emoji.command()
    @commands.has_permissions(manage_emojis=True)
    async def create(self, ctx: commands.Context, url: str, name: str):

        """
        Creates an emoji by link.
        """

        name = name or "emoji"

        async with ctx.typing():
            async with self.bot.session.get(url) as data:
                emoji = await data.read()
                emote = await ctx.guild.create_custom_emoji(name=name, image=emoji)
                await ctx.send(emote)

    @_emoji.command()
    @commands.has_permissions(manage_emojis=True)
    async def delete(self, ctx: commands.Context, name: Union[disnake.Emoji, int]):

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


def setup(bot):
    bot.add_cog(Utilities(bot))
