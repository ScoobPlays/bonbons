from disnake.ui import Select, View
from disnake import Embed, Interaction, MessageInteraction, Color, Embed, SelectOption
from disnake.ext.commands import Context, Bot, Group, Command
from utils.paginators import Paginator

class HelpCommandDropdown(Select):
    def __init__(
        self, ctx: Context, bot: Bot, embed: Embed
    ) -> None:
        self.ctx = ctx
        self.bot = bot
        self.embed = embed

        options = []

        for cog in self.bot.cogs:

            cog = self.bot.get_cog(cog)
            if cog.qualified_name in [
                "Jishaku",
                "Owner",
                "Emojis",
                "Tasks",
                "Docs",
            ]:
                continue

            options.append(
                SelectOption(
                    label=cog.qualified_name,
                    description=cog.description,
                    emoji=cog.emoji if cog.emoji else None,
                )
            )
        options.append(
            SelectOption(
                label="Home", description="Go back to the main help page.", emoji="🏠"
            )
        )

        super().__init__(
            placeholder="Choose a category!",
            min_values=1,
            max_values=1,
            options=options,
            row=0
        )
        self.commands = []
        self.embeds = []


    def _get_options(self):
        ...


    async def get_embed(self, title: str, description: str, _commands) -> list:
        
        """
        Extracts all of a category's commands, groups, then edits them to append them into a list for future usage.
        """

        for command in _commands:
            if isinstance(command, Group):
                for cmd in command.commands:
                    [self.commands.append({"name": f"{command.name} {cmd.name}", "brief": cmd.description}) for cmd in command.commands]

                self.commands.append(
                    {
                        "name": command.name,
                        "brief": command.description,
                    }
                )
                break

            if isinstance(command, Command):
                self.commands.append(
                    {"name": command.name, "brief": command.description or command.help}
                )

        return self.commands

    async def do_paginate(self, title: str, description: str, data, per_page: int, interaction: MessageInteraction) -> None:

        embeds = []

        for i in range(0, len(data), per_page):
            embed = Embed(
                title=title,
                description=description,
                colour=Color.greyple(),
            )
            for res in data[i : i + per_page]:
                embed.add_field(
                    name=res["name"],
                    value=res["brief"],
                    inline=False,
                )

            embeds.append(embed)

        for index, embed in enumerate(embeds):
            embed.set_footer(text=f"Page {index+1}/{len(embeds)}")

        self.embeds = embeds

        view = Paginator(self.ctx, self.embeds, timeout=40, embed=True, row=1)
        view.add_item(self)

        view.msg = await interaction.edit_original_message(
            content=None, embed=self.embeds[0], view=view
        )
        self.embeds = None

    async def callback(self, interaction: MessageInteraction) -> None:

        if self.values[0] == "NSFW" and not interaction.channel.is_nsfw():
            return await interaction.response.send_message("You can only view this category in an NSFW channel.", ephemeral=True)

        await interaction.response.defer()

        if self.values[0] == "Home":
            return await interaction.edit_original_message(content=None, embed=self.embed)        

        cog = self.bot.get_cog(self.values[0])

        await self.do_paginate(
            "Category Help",
            cog.description,
            await self.get_embed(
                "Category Help", cog.description, cog.get_commands()
            ),
            7,
            interaction,
        )
        self.commands = []


class HelpCommandMenu(View):
    def __init__(self, ctx: Context, bot: Bot, embed: Embed):
        super().__init__(timeout=40)
        self.ctx = ctx
        self.bot = bot
        self.embed = embed
        self.add_item(HelpCommandDropdown(self.ctx, self.bot, self.embed))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.author != self.ctx.author:
            await interaction.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False

        return True

    async def on_timeout(self):
        await self.msg.edit(view=None)