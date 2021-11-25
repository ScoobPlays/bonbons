from disnake.ext import commands
from utils.secrets import db
from utils.paginator import Paginator

class NFT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nft = db["nft"]


    @commands.group(invoke_without_command=True)
    async def nft(self, ctx):
        await ctx.send_help("nft")

    @nft.command()
    async def create(self, ctx, link, *, name):
        data = await self.nft.find({}).to_list(1000)

        the_id = len(data) + 1

        await self.nft.insert_one(
            {"name": name, "link": link, "owner": ctx.author.id, "_id": the_id}
            )
        await ctx.send("Your NFT has been created.")

    @nft.command()
    async def show(self, ctx, name):
        data = await self.nft.find_one({"name": name})
        await ctx.send(data["link"])

    @nft.command()
    async def browse(self, ctx):
        da = []
        data = await self.nft.find({}).to_list(1000)
        for item in data:
            da.append(item["link"])
        print(da)
        await ctx.send(da[0], view=Paginator(da))


def setup(bot):
    bot.add_cog(NFT(bot))