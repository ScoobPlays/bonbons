import disnake #For embeds (unsed import as of now)
from disnake.ext import commands
import pymongo

cluster = pymongo.MongoClient(
    "mongodb+srv://<username>:<password>@cluster0.s0wqa.mongodb.net/discord?retryWrites=true&w=majority"
)


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = cluster["discord"]
        self.tags = self.db["tags"]

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, command: str = None):
        if not command:
            return await ctx.send("placeholder uwu")
        else:
            data = self.tags.find_one({"name": command})
            print(data)
            await ctx.send(data["content"])

    @tag.command()
    async def create(self, ctx, name: str, *, content: str):
        await ctx.send(f"Sweet! You created a tag called {name}!")
        data = {"owner": ctx.author.id, "name": name, "content": content}
        self.tags.insert_one(data)

    @tag.command()
    async def info(self, ctx, command=None):
        data = self.tags.find_one({"name": command})
        await ctx.send(
            f"""
      Owner: <@{data["owner"]}>
      """
        )


def setup(bot):
    bot.add_cog(Tags(bot))
