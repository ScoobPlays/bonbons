import disnake
from disnake.ext import commands
import random unused
import pymongo
from datetime import datetime

cluster = pymongo.MongoClient(
    "mongodb+srv://<username>:<password>@cluster0.s0wqa.mongodb.net/discord?retryWrites=true&w=majority"
)


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = "."
        self.db = cluster["discord"]
        self.tags = self.db["tags"]

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def tag(self, ctx: commands.Context, command: str = None):
        if not command:
            help = disnake.Embed(title="Tags")
            help.add_field(
                name="tag <tag>",
                value="Displays a tag. (shows this embed if no arguments were passed)",
                inline=False,
            )
            help.add_field(
                name="tag create <name> [content]", value="Creates a tag.", inline=False
            )
            help.add_field(
                name="tag delete <tag>", value="Deletes a tag. (buggy)", inline=False
            )
            help.add_field(
                name="tag info <tag>",
                value="Gives information about a tag.",
                inline=False,
            )
            help.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            return await ctx.send(embed=help)
        else:
            data = self.tags.find_one({"name": command})
            print(data)
            await ctx.send(data["content"])

    @tag.command()
    @commands.guild_only()
    async def create(self, ctx: commands.Context, name: str, *, content: str):
        try:
            await ctx.send(f"Tag was successfully created!")
            data = {
                "owner": ctx.author.id,
                "name": name,
                "content": content,
                "created_at": int(ctx.message.created_at.timestamp()),
            }
            self.tags.insert_one(data)
        except Exception as e:
            print(e)

    @tag.command(aliases=["remove"])
    @commands.guild_only()
    @commands.has_any_role(902390891937939496)
    async def delete(self, ctx: commands.Context, tag: str = None):
        try:
            await ctx.send(f'Tag "{tag}" was deleted.')
            self.tags.delete_one({"name": tag})
        except Exception as e:
            print(e)

    @tag.command(aliases=["clear all"])
    @commands.guild_only()
    @commands.has_any_role(902390891937939496)
    async def clear(self, ctx: commands.Context):
        try:
            data = self.tags.delete_many({})
            await ctx.send(f"**{data.deleted_count}** tag(s) were deleted.")
            print(f"{data.deleted_count} documents were deleted.")
        except Exception as e:
            print(e)

    @tag.command()
    @commands.guild_only()
    async def info(self, ctx: commands.Context, tag: str = None):
        try:
            data = self.tags.find_one({"name": tag})
            print(data)

            embed = disnake.Embed(title=f"Tag Information", timestamp=datetime.utcnow())
            embed.add_field(name="Owner", value=f"<@{data['owner']}>", inline=False)
            embed.add_field(
                name="Created",
                value=f"<t:{data['created_at']}:F> (<t:{data['created_at']}:R>)",
                inline=False,
            )
            embed.set_footer(text=f"Displaying information for {tag}.")
            await ctx.send(embed=embed)

        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Tags(bot))
