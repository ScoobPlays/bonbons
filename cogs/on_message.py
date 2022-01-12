import disnake
from disnake.ext import commands


class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def github_link(self, message: disnake.Message):
        if str(message.channel.type) != "text":
            return
        if message.guild.id != 926115595307614249:
            return

        for text in message.content.split():
            if text.startswith("##"):
                await message.channel.send(
                    f"https://github.com/CaedenPH/Jarvide/pull/{text.replace('##', '')}"
                )
                break

    @commands.Cog.listener("on_message")
    async def message_increment(self, message: disnake.Message):

        if message.author.bot:
            return

        if str(message.channel.type) != "text":
            return

        db = self.bot.mongo["discord"]["messages"]

        data = await db.find_one({"_id": message.author.id})

        if data is None:
            await db.insert_one(
                {"_id": message.author.id, "messages": 1, "name": str(message.author)}
            )

        if data is not None:
            await db.update_one({"_id": message.author.id}, {"$inc": {"messages": 1}})


def setup(bot):
    bot.add_cog(OnMessage(bot))
