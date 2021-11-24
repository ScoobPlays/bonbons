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

    async def send_thank(self, ctx, member, reason):
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
        self, ctx: commands.Context, member: disnake.Member, *, reason: Optional[str]
    ):

        """
        Thank a member for something.
        """

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
                new_receiver = await self.thank.find_one({
                    "_id": ctx.author.id
                    })

                new_sent = new_receiver["sent"] + 1
                await self.thank.update_one(new_receiver, {"$set": {"sent": new_sent}})

            if not receiver:
                await self.thank.insert_one(
                    {
                        "_id": member.id,
                        "sent": 0,
                        "received": 0,
                    }
                )
                new_find = await self.thank.find_one({
                    "_id": member.id
                })

                new_received = new_find["received"] + 1
                await self.thank.update_one(new_find, {"$set": {"received": new_received}})

            if author and receiver:
                sent = author["sent"] + 1
                received = receiver["received"] + 1

            await self.thank.update_one(author, {"$set": {"sent": sent}})
            await self.thank.update_one(receiver, {"$set": {"received": received}})

        except UnboundLocalError:
            return

    @thank.command(name="stats")
    async def thank_stats(self, ctx, member: disnake.Member = None):
        """
        Display a member's stats.
        """

        member = member or ctx.author

        data = await self.thank.find_one({"_id": member.id})
        
        if not data:
            return await ctx.send(
                embed=disnake.Embed(
                    description="That member does not have any stats yet.",
                    color=disnake.Color.greyple()
                )
            )
        await ctx.send(
            embed=disnake.Embed(
                title=f"{member.display_name}'s Stats", color=disnake.Color.greyple()
            )
            .add_field(name="Thanks Sent", value=data["sent"], inline=False)
            .add_field(name="Thanks Received", value=data["received"], inline=False)
        )


def setup(bot):
    bot.add_cog(Thank(bot))
