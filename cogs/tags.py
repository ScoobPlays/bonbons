import disnake
from disnake.ext import commands
import pymongo
from datetime import datetime
from utils import mongoclient

cluster = pymongo.MongoClient(mongoclient)

class Tags(commands.Cog, description="Commands related to tags."):
    def __init__(self, bot):
        self.bot = bot
        self.db = cluster["discord"]
        self.tags = self.db["tags"]

    @commands.command()
    async def tags(self, ctx):
        """Returns all the tags in the database"""
        all_tags = []
        
        for tags in self.tags.find({}):
            all_tags.append(tags["name"])
        await ctx.send(embed=disnake.Embed(description=", ".join(all_tags)))

    @commands.slash_command()
    @commands.guild_only()
    async def tag(self, inter, tag: str = None):
        pass

    @commands.slash_command(name="tags")
    async def tags_slash(self, inter):
        """Returns all the tags in the database"""
        all_tags = []
        
        for tags in self.tags.find({}):
            all_tags.append(tags["name"])
        await inter.response.send_message(
            embed=disnake.Embed(description=", ".join(all_tags)),
            ephemeral=False
            )

    @tag.sub_command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def delete(self, inter, tag: str):
        """Deletes a tag"""
        try:
            data = self.tags.find_one({"name": tag})

            if not data:
                return await inter.response.send_message(f'Tag was not found.')

            await inter.response.send_message(f'Tag was deleted.')
            self.tags.delete_one(data)
        except Exception:
            return await inter.response.send_message(embed=disnake.Embed(description="Missing permissions."), ephemeral=True)

    @tag.sub_command()
    @commands.guild_only()
    async def show(self, inter, name: str):
        """Displays a tag"""
        data = self.tags.find_one({"name": name})

        if not data:
            return await inter.response.send_message(f"That is not a valid tag.")

        await inter.response.send_message(f"{data['content']}")

    @tag.sub_command()
    @commands.guild_only()
    async def info(self, inter, tag: str):
        """Gives information about a tag"""
        try:
            data = self.tags.find_one({"name": tag})
            print(data)

            embed = disnake.Embed(title=f"{tag} Information", timestamp=datetime.utcnow())
            embed.add_field(name="Owner", value=f"<@{data['owner']}>", inline=False)
            embed.add_field(
                name="Created",
                value=f"<t:{data['created_at']}:F> (<t:{data['created_at']}:R>)",
                inline=False,
            )
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
                f'Tag was created.', ephemeral=False
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