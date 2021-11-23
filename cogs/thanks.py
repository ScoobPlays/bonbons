from utils.secrets import thank
from disnake.ext import commands
import random
import disnake
from typing import Optional

facepalms = ("🤦‍♂️", "🤦‍♀️", "🤦")


class Thank(commands.Cog, description="Compliment related commands."):
    def __init__(self, bot):
        self.bot = bot
        self.thank = thank

    @commands.group(invoke_without_command=True)
    async def thank(
        self, ctx: commands.Context, member: disnake.Member, *, reason: Optional[str]
    ):

        """
        Thank a member for something.

        .thank <member> [reason]
        """

        if member == ctx.author:
            return await ctx.send(
                embed=disnake.Embed(
                    description=f"Why do you wanna thank yourself {random.choice(facepalms)}",
                    color=disnake.Color.red(),
                )
            )

        if reason:
            if len(reason) < 5 or len(reason) > 100:
                return await ctx.send(
                    embed=disnake.Embed(
                        description=f"A reason cannot be {'smaller than 5 characters.' if len(reason) < 5 else 'bigger than 100 characters.'}",
                        color=disnake.Color.red(),
                    )
                )
        await ctx.send(
            embed=disnake.Embed(
                description=f"You thanked {member.mention}!",
                color=disnake.Color.greyple(),
            )
        )

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

        if not receiver:
            await self.thank.insert_one(
                {
                    "_id": member.id,
                    "sent": 0,
                    "received": 1,
                }
            )

        sent = author["sent"] + 1
        received = receiver["received"] + 1

        await self.thank.update_one(author, {"$set": {"sent": sent}})
        await self.thank.update_one(receiver, {"$set": {"received": received}})

    @thank.command(name="stats")
    async def thank_stats(self, ctx, member: disnake.Member = None):
        """
        Display a member's stats.

        .thank stats [member]
        """

        member = member or ctx.author

        data = await self.thank.find_one({"_id": member.id})
        await ctx.send(
            embed=disnake.Embed(
                title=f"{member.display_name}'s Stats", color=disnake.Color.greyple()
            )
            .add_field(name="Thanks Sent", value=data["sent"], inline=False)
            .add_field(name="Thanks Received", value=data["received"], inline=False)
        )


def setup(bot):
    bot.add_cog(Thank(bot))
