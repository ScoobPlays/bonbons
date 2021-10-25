import disnake
from disnake.ext import commands
import random
import pymongo

cluster = pymongo.MongoClient(
    "mongodb+srv://<username>:<password>@cluster0.s0wqa.mongodb.net/discord?retryWrites=true&w=majority"
)


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = cluster["discord"]
        self.economy = self.db["economy"]

    async def open_account(self, member: disnake.Member):
        doc = self.economy.find_one({"_id": member.id})

        if doc != None:
            print(doc)
        else:
            print(doc)
            post = {"_id": member.id, "money": 0}
            self.economy.insert_one(post)

    @commands.command(aliases=("bal"))
    async def balance(self, ctx):
        await self.open_account(ctx.author)

        query = self.economy.find_one({"_id": ctx.author.id})
        print(query)

        money = query["money"]

        await ctx.send(f"You have {money} coins!")

    @commands.command()
    async def work(self, ctx):
        try:
            await self.open_account(ctx.author)
            earnings = random.randrange(100)
            print(earnings)

            await ctx.send(f"You worked for {earnings} coins!")

            found = self.economy.find_one({"_id": ctx.author.id})
            money = found["money"] + earnings
            self.economy.update_one({"_id": ctx.author.id}, {"$set": {"money": money}})
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Economy(bot))
