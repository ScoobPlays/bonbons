from discord.ext.commands import Cog, Context, command
from utils.bot import Bonbons
from utils.models import UserModel
from discord import Embed, Color, Member

class Economy(Cog):
    def __init__(self, bot: Bonbons):
        self.bot = bot

    @staticmethod
    async def _get_user(member: Member):
        user = await UserModel.filter(id=member.id).first()

        if user is None:
            await UserModel.create(member.id, 0, 0 , 1000)

        return user

    @command(name="balance", aliases=["bal", "cash"])
    async def balance(self, ctx: Context, member: Member=None):

        member = member or ctx.author

        user = await self._get_user(member)
        
        embed = Embed(title=f"{member.name}'s balance", color=Color.random())
        embed.add_field(name="Balance", value=f"${user.balance:,}" if user.balance else "0")
        embed.add_field(name="Bank", value=f"${user.bank:,}/{user.bank_limit:,}" if user.bank else "0")

        await ctx.send(embed=embed)


    @command(name="deposit", aliases=["dep"])
    async def deposit(self, ctx: Context, amount: int):
        member = member or ctx.author

        user = await self._get_user(member)
        
        if amount > user.balance:
            return await ctx.send("You don't have enough money to deposit that much.")

        if user.bank + amount > user.bank_limit:
            return await ctx.send("You can't deposit that much in your bank.")

        user.bank += amount
        await user.save()
        await ctx.send(f"Deposited ${amount:,} to your bank.")

def setup(bot: Bonbons) -> None:
    bot.add_cog(Economy(bot))