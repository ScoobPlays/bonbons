import discord
from discord.ext import commands

from utils.models import UserModel


class Economy(commands.Cog, description="Everyones favorite module!"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _get_user(self, member: discord.Member) -> UserModel:
        user = await UserModel.filter(id=member.id).first()

        if user is None:
            user = await UserModel.create(
                id=member.id, balance=0, bank=0, bank_limit=1000
            )
            return user

        return user

    @commands.command(name="balance", aliases=["bal", "cash"])
    async def balance(
        self, ctx: commands.Context, member: discord.Member = None
    ) -> None:

        member = member or ctx.author

        user = await self._get_user(member)

        embed = discord.Embed(
            title=f"{member.name}'s balance", color=discord.Color.random()
        )
        embed.add_field(name="Balance", value=f"${user.balance:,}")
        embed.add_field(name="Bank", value=f"${user.bank:,}/{user.bank_limit:,}")

        await ctx.send(embed=embed)

    @commands.command(name="deposit", aliases=["dep"])
    async def deposit(self, ctx: commands.Context, amount: int) -> None:

        user = await self._get_user(ctx.author)

        if amount > user.balance:
            return await ctx.send("You don't have enough money to deposit that much.")

        if user.bank + amount > user.bank_limit:
            return await ctx.send("You can't deposit that much money.")

        user.bank += amount
        await user.save()
        await ctx.send(f"Deposited ${amount:,} to your bank.")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Economy(bot))
