from disnake.ui import Select, View, button
from disnake import Embed, MessageInteraction, Color, SelectOption, ButtonStyle
from disnake.ext.commands import Context, Bot, Group, Command


BUTTON_ROW = 1

class HelpMenuPaginator(View):
    def __init__(
        self, ctx: Context, messages: list, *, embed: bool = False, timeout: int = 60, row: int=0
    ):
        super().__init__(timeout=timeout)
        self.messages = messages
        self.embed = embed
        self.current_page = 0
        self.ctx = ctx
        self.row = row
        self.add_rows()

    def add_rows(self) -> None:
        global BUTTON_ROW

        BUTTON_ROW = self.row

    async def on_timeout(self) -> None:
        await self.msg.edit(view=None)

    async def interaction_check(self, inter: MessageInteraction) -> bool:
        if inter.author.id != self.ctx.author.id:
            await inter.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False
        return True

    async def show_page(self, inter: MessageInteraction, page: int):
        if page >= len(self.messages):
            self.current_page = 0
        else:
            self.current_page = page

        data = self.messages[self.current_page]

        if self.embed:
            await inter.edit_original_message(embed=data, view=self)
        if not self.embed:
            await inter.edit_original_message(content=data, view=self)

    @button(label="<<", style=ButtonStyle.grey, row=BUTTON_ROW)
    async def back_two(self, button: Button, inter: MessageInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - self.current_page)

    @button(label="Back", style=ButtonStyle.blurple, row=BUTTON_ROW)
    async def back_one(self, button: Button, inter: MessageInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @button(label="Next", style=ButtonStyle.blurple, row=BUTTON_ROW)
    async def next_one(self, button: Button, inter: MessageInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)

    @button(label="️>>", style=ButtonStyle.grey, row=BUTTON_ROW)
    async def next_two(self, button: Button, inter: MessageInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - self.current_page - 1)

def _get_options(bot: Bot):
    options = []

    for cog in bot.cogs:

        cog = bot.get_cog(cog)
    
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
                emoji=cog.emoji,
                )
                )
    options.append(
        SelectOption(
            label="Home", description="Go back to the main help page.", emoji="🏠"
            )
            )

    return options


class HelpCommandDropdown(Select):
    def __init__(
        self, ctx: Context, bot: Bot, embed: Embed
    ) -> None:
        super().__init__(
            placeholder="Choose a category!",
            min_values=1,
            max_values=1,
            options=_get_options(bot),
            row=0
        )
        self.ctx = ctx
        self.bot = bot
        self.embed = embed
        self._commands = []
        self.embeds = []


    async def _get_embed(self, title: str, description: str, _commands) -> list:
        
        """
        Extracts all of a category's commands, groups, then edits them to append them into a list for future usage.
        """

        for command in _commands:
            if isinstance(command, Group):
                for cmd in command.commands:
                    [self._commands.append({"name": f"{command.name} {cmd.name}", "brief": cmd.description}) for cmd in command.commands]

                self._commands.append(
                    {
                        "name": command.name,
                        "brief": command.description,
                    }
                )
                break

            if isinstance(command, Command):
                self._commands.append(
                    {"name": command.name, "brief": command.description or command.help}
                )

        return self._commands

    async def paginate(self, title: str, description: str, data, per_page: int, interaction: MessageInteraction) -> None:

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

        view = HelpMenuPaginator(self.ctx, self.embeds, timeout=40, embed=True, row=1)
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

        await self.paginate(
            "Category Help",
            cog.description,
            await self._get_embed(
                "Category Help", cog.description, cog.get_commands()
            ),
            7,
            interaction,
        )
        self._commands = []


class HelpCommandMenu(View):
    def __init__(self, ctx: Context, bot: Bot, embed: Embed):
        super().__init__(timeout=40)
        self.ctx = ctx
        self.bot = bot
        self.embed = embed
        self.add_item(HelpCommandDropdown(self.ctx, self.bot, self.embed))

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False

        return True

    async def on_timeout(self):
        await self.msg.edit(view=None)