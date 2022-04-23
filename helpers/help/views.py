from discord import Color, Embed, SelectOption
from discord.ext.commands import Command, Context, Group
from discord.ui import Select, View

from helpers.paginator import HelpMenuPaginator
from helpers.bot import Bonbons

BUTTON_ROW = 1


class HelpCommandDropdown(Select):
    def __init__(self, ctx: Context, bot: Bonbons, embed: Embed) -> None:
        super().__init__(
            placeholder="Select a category..",
            min_values=1,
            max_values=1,
            row=0,
        )
        self.ctx = ctx
        self.embed = embed
        self._commands = []
        self.embeds = []
        self.bot = bot

        self.initialize()

    def initialize(self) -> None:
        for cog in self.bot.cogs:

            cog = self.bot.get_cog(cog)

            if cog.qualified_name in self.bot.ignored_cogs:
                continue

            self.append_option(
                SelectOption(
                    label=cog.qualified_name,
                    description=cog.description,
                )
            )

        self.append_option(
            SelectOption(label="Home", description="Go back to the main help page.")
        )

    async def get_embed(self, title: str, description: str, _commands) -> list:
        for command in _commands:
            if isinstance(command, Group):
                for cmd in command.commands:
                    self._commands.append(
                        {
                            "name": f"{command.name} {cmd.name}",
                            "brief": cmd.description or cmd.help or "...",
                        }
                    )

                self._commands.append(
                    {
                        "name": command.name,
                        "brief": command.description or command.help,
                    }
                )
                break

            if isinstance(command, Command):
                self._commands.append(
                    {
                        "name": command.name,
                        "brief": command.description or command.help or "...",
                    }
                )

        return self._commands

    async def paginate(
        self,
        title: str,
        description: str,
        data,
        per_page: int,
        interaction,
    ) -> None:

        embeds = []
        prefix = self.ctx.prefix

        for i in range(0, len(data), per_page):
            embed = Embed(
                title=title,
                description=description,
                colour=Color.og_blurple(),
            )
            for res in data[i : i + per_page]:
                embed.add_field(
                    name=res["name"],
                    value=res["brief"],
                    inline=False,
                )

            embeds.append(embed)

        for index, embed in enumerate(embeds):
            embed.title += f" Page {index+1}/{len(embeds)}"
            embed.set_footer(
                text=f"Use {prefix}help [command] for more info on a command."
            )

        view = HelpMenuPaginator(self.ctx, embeds, timeout=60, embed=True)
        view.add_item(self)

        if self.ctx.author.id != interaction.user.id:
            view.msg = await interaction.response.send_message(
                content=None, embed=embeds[0], view=view, ephemeral=True
            )
            embeds = None
            return

        view.msg = await interaction.edit_original_message(
            content=None, embed=embeds[0], view=view
        )

        embeds = None

    async def callback(self, interaction) -> None:

        await interaction.response.defer()

        if self.values[0] == "Home":
            return await interaction.edit_original_message(
                content=None, embed=self.embed
            )

        cog = self.ctx.bot.get_cog(self.values[0])

        await self.paginate(
            "Category Help",
            cog.description,
            await self.get_embed("Category Help", cog.description, cog.get_commands()),
            7,
            interaction,
        )
        self._commands = []


class HelpCommandMenu(View):
    def __init__(self, ctx: Context, bot: Bonbons, embed: Embed) -> None:
        super().__init__(timeout=None)
        self.add_item(HelpCommandDropdown(ctx, bot, embed))
        self.ctx = ctx

    async def interaction_check(self, interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False
        return True

    async def on_timeout(self) -> None:
        await self.msg.edit(view=None)
