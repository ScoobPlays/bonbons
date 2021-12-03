from disnake.ext import commands
from utils.env import db
from utils.paginator import Paginator
import disnake
from typing import Union, List


class ProfileView(disnake.ui.View):
    def __init__(self, messages: List):
        super().__init__()
        self.messages = messages

    @disnake.ui.button(label="Display NFTs")
    async def display_nfts(self, button, inter):
        await inter.response.defer()
        await inter.edit_original_message(
            embed=None, content=self.messages[0], view=Paginator(self.messages)
        )


class NFT(commands.Cog, description="NFT related commands."):
    def __init__(self, bot):
        self.bot = bot
        self.nft = db["nft"]

    @commands.group(invoke_without_command=True)
    async def nft(self, ctx):
        """The base command for nft."""
        await ctx.send_help("nft")

    @nft.command()
    async def create(self, ctx, link, *, name):
        """Create's an NFT."""
        if not link.endswith(".png") or link.endswith(".gif"):
            return await ctx.send("The link must end with `png` or `gif`.")
        data = await self.nft.find({}).to_list(1000)

        the_id = len(data) + 1

        find_link = await self.nft.find_one({"link": link})
        find_name = await self.nft.find_one({"name": name})

        if find_link or find_name:
            return await ctx.send(f"An NFT with that name/link already exists.")

        await self.nft.insert_one(
            {"name": name, "link": link, "owner": ctx.author.id, "_id": the_id}
        )
        await ctx.send("Your NFT has been created.")

    @nft.command()
    async def profile(self, ctx, member: disnake.Member = None):
        """Display NFT stat's for a member."""

        member = member or ctx.author
        data = await self.nft.find({}).to_list(1000)

        nfts = []
        links = []

        for item in data:
            if item["owner"] == member.id:
                nfts.append(item["_id"])
                links.append(item["link"])

        await ctx.send(
            embed=disnake.Embed(
                title=f"{member}'s Profile",
                description=f"NFTS: {nfts}",
                color=disnake.Color.greyple(),
            ),
            view=ProfileView(links),
        )

    @nft.command()
    async def lookup(self, ctx, name: Union[int, str]):
        """Find's an NFT by name/id."""

        data = await self.nft.find_one({"name": name}) or await self.nft.find_one(
            {"_id": name}
        )

        if not data:
            return await ctx.send(f"That NFT does not exist.")
        await ctx.send(
            embed=disnake.Embed(
                title=data["name"],
                description=f"Displaying `{data['name']}` by <@{data['owner']}> (ID: {data['_id']})",
                color=disnake.Color.blurple(),
            ).set_image(url=data["link"])
        )

    @nft.command()
    async def browse(self, ctx):
        """Browse all the NFTs."""

        total_nfts = []
        data = await self.nft.find({}).to_list(1000)
        for item in data:
            total_nfts.append(item["link"])

        await ctx.send(total_nfts[0], view=Paginator(total_nfts))

    @nft.command()
    async def buy(self, ctx, name: Union[int, str]):

        """Buy an NFT."""

        data = await self.nft.find_one({"name": name}) or await self.nft.find_one(
            {"_id": name}
        )

        if not data:
            return await ctx.send(f"That NFT does not exist.")

        await ctx.send(f"You bought `{data['name']}` (ID: {data['_id']})")
        await self.nft.update_one(data, {"$set": {"owner": ctx.author.id}})


def setup(bot):
    bot.add_cog(NFT(bot))
