import disnake
from disnake.ext import commands
from datetime import datetime
from utils import cluster, tags_autocomp


class Tags(commands.Cog, description="Commands related to tags."):
    def __init__(self, bot):
        self.bot = bot
        self.db = cluster["discord"]

    @commands.command()
    async def tags(self, ctx):
        """Returns all the tags in the database"""
        try:
            self.tags = self.db[str(ctx.guild.id)]

            all_tags = []

            for tags in self.tags.find({}):
                all_tags.append(tags["name"])
                await ctx.send(embed=disnake.Embed(description=", ".join(all_tags)))
        except disnake.HTTPException:
            await ctx.send(
                embed=disnake.Embed(
                    "There are no tags in the current guild.", color=disnake.Color.red()
                )
            )

    @commands.slash_command()
    @commands.guild_only()
    async def tag(self, inter, tag: str = None):
        pass

    @commands.slash_command(name="tags")
    async def tags_slash(self, inter):
        """Returns all the tags in the database"""

        try:
            self.tags = self.db[str(inter.guild.id)]

            all_tags = []

            for tags in self.tags.find({}):
                all_tags.append(tags["name"])
                await inter.response.send_message(
                    embed=disnake.Embed(description=", ".join(all_tags)),
                    ephemeral=False,
                )
        except disnake.HTTPException:
            await inter.response.send_message(
                embed=disnake.Embed(
                    "There are no tags in the current guild.",
                    color=disnake.Color.red(),
                    ephemeral=False,
                )
            )

    @tag.sub_command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def delete(self, inter, name: str = commands.param(autocomp=tags_autocomp)):
        """Deletes a tag"""
        try:
            self.tags = self.db[str(inter.guild.id)]
            data = self.tags.find_one({"name": name})

            if not data:
                return await inter.response.send_message(f"Tag was not found.")

            await inter.response.send_message(f"Tag was deleted.")
            self.tags.delete_one(data)
        except Exception as e:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description="Missing permissions.", color=disnake.Color.red()
                ),
                ephemeral=True,
            )

    @tag.sub_command()
    @commands.guild_only()
    async def show(self, inter, name: str = commands.param(autocomp=tags_autocomp)):
        """Displays a tag"""
        self.tags = self.db[str(inter.guild.id)]
        data = self.tags.find_one({"name": name})

        if not data:
            return await inter.response.send_message(f"That is not a valid tag.")

        await inter.response.send_message(f"{data['content']}")

    @tag.sub_command()
    @commands.guild_only()
    async def info(self, inter, name: str = commands.param(autocomp=tags_autocomp)):
        """Gives information about a tag"""
        try:
            self.tags = self.db[str(inter.guild.id)]
            data = self.tags.find_one({"name": name})

            if not data:
                return await inter.response.send_message(
                    embed=disnake.Embed(
                        description="That is not a valid tag.",
                        color=disnake.Color.red(),
                    )
                )

            author = data["owner"]

            embed = disnake.Embed(title=f"Tag Information", timestamp=datetime.utcnow())
            embed.add_field(
                name="Owner", value=f"<@{data['owner']}> (`{author.id}`)", inline=False
            )
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
            self.tags = self.db[str(inter.guild.id)]
            found = self.tags.find_one({"name": name})
            if found:
                return await inter.response.send_message(
                    f"A tag with that name already exists.", ephemeral=False
                )

            await inter.response.send_message(f"Tag was created.", ephemeral=False)

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
