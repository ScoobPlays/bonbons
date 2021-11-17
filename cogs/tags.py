import disnake
from disnake.ext import commands
from datetime import datetime
from utils.mongo import cluster


class Tags(commands.Cog, description="Commands related to tags."):
    def __init__(self, bot):
        self.bot = bot
        self.db = cluster["discord"]

    async def tags_autocomp(inter, input: str) -> str:
        db_tags = cluster["discord"][str(inter.guild.id)]
        find_tags = await db_tags.find({}).to_list(10000)

        all_tags = []

        for tags in find_tags:
            all_tags.append(tags["name"])

        return [tag for tag in all_tags if input.lower() in tag.lower()]

    @commands.slash_command()
    @commands.guild_only()
    async def tag(self, inter) -> None:
        """The base command for tag."""
        pass

    @commands.command()
    async def tags(self, ctx) -> None:
        """Returns all the tags in the guild."""
        try:
            index = 0
            tags_embed = disnake.Embed(
                title="Tags", description="", color=disnake.Color.greyple()
            )
            self.tags = self.db[str(ctx.guild.id)]

            tags = await self.tags.find({}).to_list(10000)

            for name in tags:
                index += 1
                tags_embed.description += f"\n{index}. {name['name']}"

            await ctx.send(embed=tags_embed)

        except Exception as e:
            print(e)

    @commands.slash_command(name="tags")
    async def tags_slash(self, inter: disnake.ApplicationCommandInteraction) -> None:

        """Returns all the tags in the guild"""

        try:
            index = 0
            tags_embed = disnake.Embed(
                title="Tags", description="", color=disnake.Color.greyple()
            )
            self.tags = self.db[str(inter.guild.id)]

            tags = await self.tags.find({}).to_list(10000)

            for name in tags:
                index += 1
                tags_embed.description += f"\n{index}. {name['name']}"

            await inter.response.send_message(embed=tags_embed, ephemeral=False)

        except Exception as e:
            print(e)

    @tag.sub_command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def delete(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.param(
            description="The tag's name to delete", autocomp=tags_autocomp
        ),
    ) -> None:
        """Delete's a tag"""
        try:
            self.tags = self.db[str(inter.guild.id)]
            data = await self.tags.find_one({"name": name})

            if not data:
                return await inter.response.send_message(f"Tag was not found.")

            await inter.response.send_message(f"Tag was deleted.")
            self.tags.delete_one(data)
        except Exception:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description="Missing permissions.", color=disnake.Color.red()
                ),
                ephemeral=True,
            )

    @tag.sub_command()
    @commands.guild_only()
    async def show(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.param(
            description="The tag's name to display", autocomp=tags_autocomp
        ),
    ) -> None:
        """Display's a tag"""
        self.tags = self.db[str(inter.guild.id)]
        data = await self.tags.find_one({"name": name})

        if not data:
            return await inter.response.send_message(f"That is not a valid tag.")

        await inter.response.send_message(f"{data['content']}")

    @tag.sub_command()
    @commands.guild_only()
    async def info(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.param(
            description="The tag's name", autocomp=tags_autocomp
        ),
    ) -> None:
        """Gives information about a tag"""
        try:
            self.tags = self.db[str(inter.guild.id)]
            data = await self.tags.find_one({"name": name})

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
    async def create(self, inter, name: str, content: str) -> None:
        """Creates a tag"""
        try:
            self.tags = self.db[str(inter.guild.id)]
            found = await self.tags.find_one({"name": name})
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
            await self.tags.insert_one(data)
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Tags(bot))
