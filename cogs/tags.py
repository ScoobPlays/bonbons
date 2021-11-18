import disnake
from disnake.ext import commands
from datetime import datetime
from utils.mongo import cluster
from utils.bonbons import Bonbons

bot = Bonbons()


class Buttons(disnake.ui.View):
    def __init__(self, bot, inter, name):
        super().__init__()
        self.bot = bot
        self.name = name
        self.db = cluster["discord"]
        self.inter = inter
        self.author = self.inter.author
        self.edit = self.inter.edit_original_message

    async def interaction_check(self, inter) -> bool:
        if inter.author.id != self.author.id:
            await inter.response.send_message(
                f"Only `{self.author.mention}` can use the buttons on this message.",
                ephemeral=True,
            )
            return False
        return True

    @disnake.ui.button(label="Content")
    async def tag_content(self, button, inter):
        self.tags = self.db[str(inter.guild.id)]

        await inter.response.send_message(
            "Alright so what do you want the change this tag's content to?",
            ephemeral=True,
        )

        msg = await self.bot.wait_for(
            "message", check=lambda m: m.author.id == inter.author.id
        )
        await msg.add_reaction("✅")
        await self.tags.update_one(self.name, {"$set": {"content": msg.content}})

        await self.edit(
            embed=disnake.Embed(
                title="Tag was Edited",
                description="Tag was successfully edited!",
                color=disnake.Color.green(),
            ),
            view=None,
        )


class Tags(commands.Cog, description="Commands related to tags."):
    def __init__(self, bot):
        self.bot = bot
        self.db = cluster["discord"]

    async def inter_autocomp(inter, input: str) -> str:
        db_tags = cluster["discord"][str(inter.guild.id)]
        find_tags = await db_tags.find({}).to_list(10000)

        all_tags = []

        for tags in find_tags:
            all_tags.append(tags["name"])

        return [tag for tag in all_tags if input.lower() in tag.lower()]

    async def context_autocomp(ctx, input: str) -> str:
        db_tags = cluster["discord"][str(ctx.guild.id)]
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
    async def edit(
        self,
        inter,
        name: str = commands.Param(
            description="The name of the tag", autocomp=inter_autocomp
        ),
    ):
        """Edit's a tag you own"""
        self.tags = self.db[str(inter.guild.id)]

        tag_data = await self.tags.find_one({"name": name})
        tag_owner = tag_data["owner"]

        if not tag_data:
            return await inter.response.send_message(
                "A tag with this name does not exist.", ephemeral=True
            )

        if tag_owner != inter.author.id:
            return await inter.response.send_message(
                "You do not own this tag.", ephemeral=False
            )

        await inter.response.send_message(
            embed=disnake.Embed(
                title="Editing a Tag",
                description="Click the button below to edit your tag.",
                color=disnake.Color.greyple(),
            ),
            view=Buttons(self.bot, inter, tag_data),
        )

    @tag.sub_command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def delete(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.param(
            description="The tag's name to delete", autocomp=inter_autocomp
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
            description="The tag's name to display", autocomp=inter_autocomp
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
            description="The tag's name", autocomp=inter_autocomp
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
