import discord
from discord import Color, Embed
from discord.ext.commands import Command, Group, HelpCommand
from helpers.paginator import Paginator

from .views import HelpCommandMenu


class CustomHelpCommand(HelpCommand):

    """
    A custom help command with a custom paginator.
    """

    def __init__(self):
        super().__init__(
            command_attrs={
                "hidden": True,
                "help": "Shows help about a category, or a command.",
            }
        )
        self.commands = []

    async def send(self, **kwargs):
        return await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping) -> None:

        value = "Use the dropdown below to navigate through my modules."

        embed = Embed(
            title="Help Menu",
            description=f"Hello! I am bonbons, I was made by sift#0410 around <t:1631859987:R>.\n\nUse the dropdown below to navigate through my modules. If you need help with a specific command, use `{self.context.clean_prefix}help [command]`.",
            color=Color.og_blurple(),
        )
        view = HelpCommandMenu(self.context, self.context.bot, embed)

        view.msg = await self.send(
            embed=embed,
            view=view,
        )

    async def paginate(
        self, title: str, description: str, data, *, per_page: int
    ) -> None:
        embeds = []

        for i in range(0, len(data), per_page):
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Color.og_blurple(),
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
                text=f"Use b!help [command] for more info on a command." # unsure on how I would make the prefix dynamic
            )

        view = Paginator(self.context, embeds, embed=True)

        view.msg = await self.send(embed=embeds[0], view=view)

    async def send_help_embed(
        self, title: str, description: str, _commands,
    ) -> None:

        for command in _commands:
            if isinstance(command, Group):
                for cmd in command.commands:
                    self.commands.append(
                        {
                            "name": f"{command.name} {cmd.name}",
                            "brief": cmd.description or cmd.help or "...",
                        }
                    )

                self.commands.append(
                    {
                        "name": command.name,
                        "brief": command.description or command.help or "...",
                    }
                )
                break

            if isinstance(command, Command):
                self.commands.append(
                    {
                        "name": command.name,
                        "brief": command.description or command.help or "...",
                    }
                )

        await self.paginate(
            title, description, self.commands, per_page=7, prefix="b!"
        )

        self.commands = []

    async def send_group_help(self, group: Group) -> None:
        return await self.send_help_embed(
            "Group Help", group.description, group.commands, self.context.clean_prefix
        )

    async def send_cog_help(self, cog: Group) -> None:
        return await self.send_help_embed(
            "Category Help",
            cog.description,
            cog.get_commands(),
            self.context.clean_prefix,
        )

    async def send_command_help(self, command: Command) -> None:
        embed = Embed(title="Command Help", color=Color.og_blurple())
        description = command.description or command.help or "..."

        embed.description = (
            f"```\n{self.get_command_signature(command)}\n```{description}"
        )

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases))

        return await self.send(embed=embed)
