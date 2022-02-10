import copy

from disnake import DMChannel, Message, Embed
from disnake.ext.commands import Bot, Cog, Context, group, guild_only

from utils.paginators import TagPages
from datetime import datetime

# TODO: implement difflib in `delete`/`get`


class Tags(Cog):

    """Tag-related commands."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.emoji = "📰"
        self.base = self.bot.mongo["tags"]
        self._tags_cache = []

    async def prepare_embed(self, ctx: Context, data: dict) -> Embed:

        owner = self.bot.get_user(data["owner"]) or await self.bot.fetch_user(data["owner"])
        embed = Embed(title=data["name"])
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
        embed.add_field(name="Owner", value=owner.mention)

        return embed

    async def get_tag(self, ctx: Context, name: str):
        db = self.base[str(ctx.guild.id)]

        tag = await db.find_one({"name": name.lower()})

        if tag is not None:
            return await ctx.send(tag["content"])

        if tag is None:
            return await ctx.send("Tag not found.")

    async def try_to_delete_tag(self, ctx: Context, name: str):
        db = self.base[str(ctx.guild.id)]

        tag_name = await db.find_one({"name": name})

        if tag_name is not None:
            if (
                ctx.author.guild_permissions.manage_channels
                or tag_name["owner"] == ctx.author.id
            ):
                return await db.delete_one({"name": name})

            return await ctx.send("You do not own this tag.")

        if tag_name is None:
            return await ctx.send("A tag with this name does not exist.")

    async def edit_tag(self, ctx: Context, name: str, content: str):

        db = self.base[str(ctx.guild.id)]
        tag_name = await db.find_one({"name": name})
        prefix = await self.bot.command_prefix(self.bot, ctx.message)

        if tag_name is None:
            return await ctx.send("A tag with that name does not exist!")

        if ctx.author.id != tag_name["owner"]:
            return await ctx.send("You do not own this tag.")

        await self.db.update_one({"name": name}, {"$set": {"content": content}})

        await ctx.send(
            f"Tag successfully edited! Do {prefix[2]}tag {name} to view the tag."
        )

    async def create_tag(self, ctx: Context, name: str, content: str):

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
            "created": int(datetime.now().timestamp())
        }

        await db.insert_one(tag_data)
        return await ctx.send(
            f"Tag successfully created. Do {prefix[2]}tag {name} to view the tag."
        )

    @group(name="tag", invoke_without_command=True, case_insensitive=True)
    @guild_only()
    async def tag(self, ctx: Context, tag: str = None):

        """Sends the help embed for the tag group, sends a tag's content if a valid tag name was passed."""

        if tag is not None:
            await self.get_tag(ctx, tag)

        if tag is None:
            await ctx.send_help("tag")

    @tag.command(name="create", aliases=["build"])
    @guild_only()
    async def create(self, ctx: Context, name: str, *, content: str):

        """Creates a tag."""

        await self.create_tag(ctx, name, content)

    @tag.command(name="info", aliases=["information"])
    @guild_only()
    async def info(self, ctx: Context, *, name: str):

        """Tells you information about a tag."""

        db = self.base[str(ctx.guild.id)]

        tag_info = await db.find_one({"name": name.lower()})

        if tag_info is not None:
            embed = self.prepare_embed(ctx, tag_info)

        if tag_info is None:
            return await ctx.reply("Not a valid tag!")

    @tag.command(name="edit", aliases=["modify"])
    @guild_only()
    async def edit(self, ctx: Context, name: str, *, content: str):

        """Tries to edit a tag you own."""

        await self.edit_tag(ctx, name, content)

    @tag.command(aliases=["list"])
    @guild_only()
    async def all(self, ctx: Context):
        
        """Tells you all the tags in the current server."""

        db = self.base[str(ctx.guild.id)]
        data = await db.find().to_list(100000)

        view = TagPages(data)

        await view.start(ctx, per_page=20)

    @tag.command(aliases=["remove"])
    @guild_only()
    async def delete(self, ctx: Context, *, name: str):

        """Deletes a tag."""

        await self.try_to_delete_tag(ctx, name)

    @Cog.listener("on_message")
    async def send_tags(self, message: Message):

        if isinstance(message.channel, DMChannel):
            return await self.bot.process_commands(message)

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
