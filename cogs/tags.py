import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import pymongo
from datetime import datetime

cluster = pymongo.MongoClient(
    "mongodb+srv://kayle:kaylebetter@cluster0.s0wqa.mongodb.net/discord?retryWrites=true&w=majority"
)


class Tags(commands.Cog, description="Commands related to tags"):
    def __init__(self, bot):
        self.bot = bot
        self.db = cluster["discord"]
        self.tags = self.db["tags"]

    @commands.slash_command()
    @commands.guild_only()
    async def tag(self, inter, tag: str = None):
        pass

    @tag.sub_command()
    @commands.guild_only()
    @commands.has_any_role(902390891937939496)
    async def delete(self, inter, tag: str):
        """Deletes a tag"""
        try:
            data = self.tags.find_one({"name": tag})

            if not data:
                return await inter.response.send_message(f'Tag "{tag}" was not found.')

            await inter.response.send_message(f'Tag "{tag}" was deleted.')
            self.tags.delete_one(data)
        except Exception as e:
            print(e)

    @tag.sub_command()
    async def show(self, inter, name: str):
        data = self.tags.find_one({"name": name})
        # if not data:
        #    return await inter.response.send_message("a")

        await inter.response.send_message(f"{data['content']}")

    @tag.sub_command()
    @commands.guild_only()
    @commands.has_any_role(902390891937939496)
    async def clear(self, inter):
        """Clears the database for all tags"""
        try:
            data = self.tags.delete_many({})
            await inter.response.send_message(
                f"**{data.deleted_count}** tag(s) were deleted."
            )
            print(f"{data.deleted_count} documents were deleted.")
        except Exception as e:
            print(e)

    @tag.sub_command()
    @commands.guild_only()
    async def info(self, inter, tag: str = Param(desc="A tag that exists")):
        """Gives information about a tag"""
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
            await inter.response.send_message(embed=embed, ephemeral=False)

        except Exception as e:
            print(e)

    @tag.sub_command()
    @commands.guild_only()
    async def create(self, inter, name: str, content: str):
        """Creates a tag"""
        try:
            found = self.tags.find_one({"name": name})
            if found:
                return await inter.response.send_message(
                    f"A tag with that name already exists.", ephemeral=False
                )

            await inter.response.send_message(
                f'Tag "{name}" was created.', ephemeral=False
            )

            data = {
                "owner": inter.author.id,
                "name": name,
                "content": content,
                "created_at": (int(datetime.utcnow().timestamp())),
            }
            self.tags.insert_one(data)
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Tags(bot))
