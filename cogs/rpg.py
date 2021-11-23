from disnake.ext import commands
from utils.secrets import db
import random

class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rpg = db["rpg"]


    @commands.slash_command()
    async def register(self, inter):
        await self.rpg.insert_one({
            "_id": inter.author.id,
            "hp": 100,
            "attack": 10,
            "money": 10
        })
        await inter.response.send_message(
            "Registered."
        )
    @commands.slash_command()
    async def hunt(self, inter):
        integer = random.randint(0, 100)
        responses = (
            f"You found a horse and sold it for ${integer}."
            f"You robbed someone and got ${integer}"
        )
        await inter.response.send_message(
            random.choice(responses)
        )
        data = await self.rpg.find_one({
            "_id": inter.author.id
        })
        money = data["money"] + integer

        await self.rpg.update_one(data, {"$set": {"money": money}})


def setup(bot):
    bot.add_cog(RPG(bot))