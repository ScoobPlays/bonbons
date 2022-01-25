from disnake.ext import commands
from utils.paginators import TagPages
import copy


class Tags(commands.Cog):
    """Tag-related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "📰"
        self.base = self.bot.mongo["tags"]
        self.cache = []

    @commands.group(name="tag", invoke_without_command=True)
    async def tag(self, ctx: commands.Context, tag: str = None):
        """Sends the help embed for the tag command group.\nIf an argument was passed then it'll send the tag content."""
        if tag is None:
            await ctx.send_help("tag")
        if tag is not None:
            await self.get_tag(ctx, tag)

    async def get_tag(self, ctx: commands.Context, name: str):
        db = self.base[str(ctx.guild.id)]

        tag = await db.find_one({"name": name})

        if tag is not None:
            return await ctx.send(tag["content"])

        if tag is None:
            return await ctx.send("A tag with this name does not exist in my database.")

    async def edit_tag(self, ctx: commands.Context, name: str, content: str):

        db = self.base[str(ctx.guild.id)]
        tag_name = await db.find_one({"name": name})
        prefix = await self.bot.command_prefix(self.bot, ctx.message)

        if tag_name is None:
            return await ctx.send("A tag with that name does not exist!")

        if ctx.author.id != tag_name["owner"]:
            return await ctx.send("You do not own this tag.")

        await self.db.update_one({"name": name}, {"$set": {"content": content}})

        await ctx.send(
            f"Tag successfully edited! Do `{prefix}tag {name}` to view the tag!"
        )

    async def create_tag(self, ctx: commands.Context, name: str, content: str):

        db = self.base[str(ctx.guild.id)]
        prefix = await self.bot.command_prefix(self.bot, ctx.message)
        tag_name = await db.find_one({"name": name})
        tag_id = len(await db.find().to_list(10000)) + 1

        if tag_name:
            return await ctx.send("A tag with this name already exists.")

        tag_data = {
            "_id": tag_id,
            "owner": ctx.author.id,
            "name": name,
            "content": content,
        }

        await db.insert_one(tag_data)
        return await ctx.send(
            f"Tag successfully created. Do `{prefix}tag {name}` to view the tag!"
        )

    @tag.command(aliases=["build"])
    async def create(self, ctx: commands.Context, name: str, *, content: str):
        """
        Creates a tag.
        """
        await self.create_tag(ctx, name, content)

    @tag.command(aliases=["modify"])
    async def edit(self, ctx: commands.Context, name: str, *, content: str):
        """Edits a tag. Only the owners of the tag can edit their tags."""
        await self.edit_tag(ctx, name, content)

    @tag.command(aliases=["list"])
    async def all(self, ctx: commands.Context):
        """Sends all the tags in the current guild."""
        db = self.base[str(ctx.guild.id)]

        view = TagPages(await db.find().to_list(10000))
        await view.start(ctx, per_page=20)

    @commands.Cog.listener("on_message")
    async def send_tags(self, message):

        ctx = await self.bot.get_context(message)

        db = self.bot.mongo["tags"][str(ctx.guild.id)]

        if (
            ctx.invoked_with
            and ctx.invoked_with.lower() not in self.bot.commands
            and ctx.command is None
        ):

            msg = copy.copy(message)

            if ctx.prefix:
                new_content = msg.content[len(ctx.prefix) :]

                if await db.find_one({"name": new_content}) is None:
                    return await self.bot.process_commands(msg)

                msg.content = f"{ctx.prefix}tag {new_content}"

                await self.bot.process_commands(msg)


def setup(bot):
    bot.add_cog(Tags(bot))
