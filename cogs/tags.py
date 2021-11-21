import disnake
from disnake.ext import commands
from datetime import datetime
from utils.mongo import cluster

class Make(disnake.ui.View):
    def __init__(self, bot, inter):
        super().__init__()
        self.interaction = inter
        self.author = self.interaction.author
        self.name = None
        self.bot = bot
        self.content = None
        self.db = cluster["discord"]

    @disnake.ui.button(label="Name", style=disnake.ButtonStyle.blurple)
    async def tag_name(self, button, inter):
        await inter.response.send_message("Alright what do you want the tag's name to be?", ephemeral=True)

        name = await self.bot.wait_for(
            "message",
            timeout = 30,
            check=lambda m: m.author.id == self.author.id and m.channel.id == inter.channel.id
            )
        self.name = name

    @disnake.ui.button(label="Cntent", style=disnake.ButtonStyle.blurple)
    async def tag_conent(self, button, inter):
        await inter.response.send_message("Okay, what do you want the tag's content to be?", ephemeral=True)
        
        content = await self.bot.wait_for(
            "message",
            timeout = 30,
            check=lambda m: m.author.id == self.author.id and m.channel.id == inter.channel.id
            )
        self.content = content

    @disnake.ui.button(label="Confirm", style=disnake.ButtonStyle.green)
    async def tag_confirm(self, button, inter):
        self.tags = self.db[str(inter.guild.id)]

        found = await self.tags.find_one({"name": self.name.content})

        if found:
            return await inter.response.send_message(
                f"Creating a tag failed. A tag with that name already exists.", ephemeral=True
                )
        
        await inter.response.send_message("Tag has been created.", ephemeral=True)

        data = {
            "owner": self.name.author.id,
            "name": self.name.content,
            "content": self.content.content,
            "created_at": (int(datetime.utcnow().timestamp())),
            }
        await self.tags.insert_one(data)


class Editing(disnake.ui.View):
    def __init__(self, bot, inter: disnake.ApplicationCommandInteraction, name: str):
        super().__init__()
        self.bot = bot
        self.name = name
        self.db = cluster["discord"]
        self.inter = inter
        self.author = self.inter.author
        self.edit = self.inter.edit_original_message

    async def interaction_check(self, inter: disnake.ApplicationCommandInteraction) -> bool:
        if inter.author.id != self.author.id:
            await inter.response.send_message(
                f"Only `{self.author.mention}` can use the buttons on this message.",
                ephemeral=True,
            )
            return False
        return True

    @disnake.ui.button(label="Content")
    async def tag_content(self, button, inter: disnake.ApplicationCommandInteraction):
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

    async def send_tag_info(self, inter, name):
        try:
            self.tags = self.db[str(inter.guild.id)]
            data = await self.tags.find_one({"name": name})

            if not data:
                return await inter.response.send_message(
                    "That is not a valid tag.",
                    ephemeral=True
                )


            embed = disnake.Embed(
                title=f"Tag Information",
                color=disnake.Color.greyple(),
                timestamp=datetime.utcnow()
                ).add_field(
                name="Owner",
                value=f"<@{data['owner']}> (`{data['owner']}`)",
                inline=False
            ).add_field(
                name="Created",
                value=f"<t:{data['created_at']}:F> (<t:{data['created_at']}:R>)",
                inline=False,
            )
            await inter.response.send_message(embed=embed, ephemeral=False)

        except Exception as e:
            print(e)

    async def inter_autocomp(inter: disnake.ApplicationCommandInteraction, input: str) -> str:
        db_tags = cluster["discord"][str(inter.guild.id)]
        find_tags = await db_tags.find({}).to_list(10000)

        all_tags = []

        for tags in find_tags:
            all_tags.append(tags["name"])

        return [tag for tag in all_tags if input.lower() in tag.lower()]

    async def context_autocomp(ctx: commands.Context, input: str) -> str:
        db_tags = cluster["discord"][str(ctx.guild.id)]
        find_tags = await db_tags.find({}).to_list(10000)

        all_tags = []

        for tags in find_tags:
            all_tags.append(tags["name"])

        return [tag for tag in all_tags if input.lower() in tag.lower()]

    @commands.slash_command()
    @commands.guild_only()
    async def tag(self, inter: disnake.ApplicationCommandInteraction) -> None:
        """The base command for tag."""
        pass

    @commands.command()
    async def tags(self, ctx: commands.Context) -> None:
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
        inter: disnake.ApplicationCommandInteraction,
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
                "You do not own this tag.", ephemeral=True
            )

        await inter.response.send_message(
            embed=disnake.Embed(
                title="Editing a Tag",
                description="Click the button below to edit your tag.",
                color=disnake.Color.greyple(),
            ),
            view=Editing(self.bot, inter, tag_data),
            ephemeral=True
        )

    @tag.sub_command(name="deelte")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def delete_tag(
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

    @tag.sub_command(name="show")
    @commands.guild_only()
    async def show_tag(
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

    @tag.sub_command(name="info")
    @commands.guild_only()
    async def tag_info(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.param(
            description="The tag's name", autocomp=inter_autocomp
        ),
    ) -> None:
        """Gives information about a tag"""

        await self.send_tag_info(inter, name)

    @tag.sub_command(name="make")
    @commands.guild_only()
    async def make_tag(self, inter: disnake.ApplicationCommandInteraction):
        """Creates a tag"""
        try:
            await inter.response.send_message(
                embed = disnake.Embed(
                    title="Making a Tag",
                    description="The process is very simple, you first click `Name` and then `Content`. Once you've done clicking the buttons you then click the `Confirm` button to confirm that you wanna create a tag.",
                    color=disnake.Color.greyple()
                ).set_footer(text="You must send a message once you've clicked a button."),
                view=Make(self.bot, inter),
                ephemeral=True
                )
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(Tags(bot))