from disnake.ext import commands
from utils.secrets import db
import random
import disnake
import pymongo

class RPG(commands.Cog, description="RPG related commands."):
    def __init__(self, bot):
        self.bot = bot
        self.rpg = db["rpg"]

    @commands.command()
    async def register(self, ctx):
        await self.rpg.insert_one(
            {"_id": ctx.author.id, "hp": 100, "attack": 10, "money": 10}
        )

        await ctx.send("Registered.")

    @commands.command()
    async def hunt(self, ctx):
        integer = random.randint(0, 100)
        responses = (
            f"You found a horse and sold it for ${integer}.",
            f"You robbed someone and got ${integer}",
        )
        await ctx.send(random.choice(responses))
        data = await self.rpg.find_one({"_id": ctx.author.id})
        money = data["money"] + integer

        await self.rpg.update_one(data, {"$set": {"money": money}})

    @commands.command()
    async def stats(self, ctx):
        data = await self.rpg.find_one({
            '_id': ctx.author.id
        })

        embed = embed=disnake.Embed(
            description=f"❤: {data['hp']}\n🗡: {data['attack']}\n💸: {data['money']}", color=disnake.Color.greyple()
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(RPG(bot))