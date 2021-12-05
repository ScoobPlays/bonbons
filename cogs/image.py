from disnake.ext import commands
from utils.env import db
from utils.paginator import EmbedPaginator
import disnake
from typing import Union


class Image(commands.Cog, description="Image related commands."):
    def __init__(self, bot):
        self.bot = bot
        self.images = db["nft"]

    @commands.group(invoke_without_command=True)
    async def image(self, ctx):
        """The base command for image."""
        await ctx.send_help("image")

    @image.command()
    async def create(self, ctx: commands.Context, link: str, *, name: str):

        """Create or upload an image!"""

        if not link.endswith(".png") or link.endswith(".gif"):
            return await ctx.send("The image link must end with `png` or `gif`.")
        data = await self.images.find({}).to_list(1000)

        the_id = len(data) + 1

        find_link = await self.images.find_one({"link": link})
        find_name = await self.images.find_one({"name": name})

        if find_link or find_name:
            return await ctx.send(f"An image with that name/link already exists.")

        await self.images.insert_one(
            {"name": name, "link": link, "owner": ctx.author.id, "_id": the_id}
        )
        await ctx.send("Your image has been created.")

    @image.command()
    async def profile(self, ctx, member: disnake.Member = None):
        """Display image stat's for a member."""

        member = member or ctx.author
        data = await self.images.find({}).to_list(10000)

        names, owners, embeds, image_ids, links = (
            [],
            [],
            [],
            [],
            [],
        )

        for item in data:
            if item["owner"] == member.id:
                image_ids.append(item["_id"])
                links.append(item["link"])
                names.append(item["name"])
                owners.append(item["owner"])

        for image_id, link, name, owner in zip(image_ids, links, names, owners):
            embeds.append(
                disnake.Embed(
                    description=f"Displaying `{name}` by <@{owner}> (ID: {image_id})",
                    color=disnake.Color.blurple(),
                ).set_image(url=link)

        await ctx.send(
            embed=disnake.Embed(
                title=f"{member}'s Profile",
                description=f"Images: {image_ids}",
                color=disnake.Color.blurple(),
            ),
            view=EmbedPaginator(ctx, embeds),
        )

    @image.command()
    async def lookup(self, ctx, name: Union[int, str]):
        """Find's an image uploaded by name/ID."""

        data = await self.images.find_one({"name": name}) or await self.images.find_one(
            {"_id": name}
        )

        if not data:
            return await ctx.send(f"That image does not exist.")
        await ctx.send(
            embed=disnake.Embed(
                title=data["name"],
                description=f"Displaying `{data['name']}` by <@{data['owner']}> (ID: {data['_id']})",
                color=disnake.Color.blurple(),
            ).set_image(url=data["link"])
        )

    @image.command()
    async def browse(self, ctx: commands.Context):
        """Browse all the uploaded images."""

        images, names, owners, ids, embeds = [], [], [], [], []

        data = await self.images.find({}).to_list(1000)
        for item in data:
            images.append(item["link"])
            names.append(item["name"])
            owners.append(item["owner"])
            ids.append(item["_id"])

        for link, name, owner, image_id in zip(images, names, owners, ids):
            embeds.append(
                disnake.Embed(
                    description=f"Displaying `{name}` by <@{owner}> (ID: {image_id})",
                    color=disnake.Color.blurple(),
                ).set_image(url=link)
            )

        await ctx.send(embed=embeds[0], view=EmbedPaginator(ctx, embeds))

    @image.command()
    async def buy(self, ctx: commands.Context, name: Union[int, str]):

        """Buy an image for free."""

        data = await self.images.find_one({"name": name}) or await self.images.find_one(
            {"_id": name}
        )

        if not data:
            return await ctx.send(f"That image does not exist.")

        await ctx.send(f"You bought `{data['name']}` (ID: {data['_id']})")
        await self.images.update_one(data, {"$set": {"owner": ctx.author.id}})


def setup(bot):
    bot.add_cog(Image(bot))
