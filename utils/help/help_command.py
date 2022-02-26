import discord
from discord.ext import commands

from utils.paginator import Paginator

from .ext import HelpEmbed
from .views import HelpCommandMenu


class CustomHelpCommand(commands.HelpCommand):
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

        value = 'Click the dropdown and pick an option! To get more help do...\n\n"help [command]"\nhelp [category]\nhelp [group]\n'

        embed = HelpEmbed(
            title="Bonbons Help Page",
            description=f"Hello! I am bonbons, I was made by sift#0410 around <t:1631859987:R>.",
        )
        embed.add_field(name="How do I get help?", value=value)

        view = HelpCommandMenu(self.context, self.context.bot, embed)

        view.msg = await self.send(
            embed=embed,
            view=view,
        )

    async def send_command_help(self, command: commands.Command) -> None:
        embed = HelpEmbed(title="Command Help")

        embed.description = (
            f"```\n{self.get_command_signature(command)}\n```\n\n{command.description}"
        )

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases))

        return await self.send(embed=embed)

    async def paginate(self, title: str, desc: str, data, *, per_page: int) -> None:
        embeds = []

        for i in range(0, len(data), per_page):
            embed = discord.Embed(
                title=title,
                description=desc,
                colour=discord.Color.greyple(),
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

        view = Paginator(self.context, embeds, embed=True)

        view.msg = await self.send(embed=embeds[0], view=view)

    async def send_help_embed(self, title: str, description: str, _commands) -> None:

        for command in _commands:
            if isinstance(command, commands.Group):
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

            if isinstance(command, commands.Command):
                self.commands.append(
                    {
                        "name": command.name,
                        "brief": command.description or command.help or "...",
                    }
                )

        await self.paginate(title, description, self.commands, per_page=7)

        self.commands = []

    async def send_group_help(self, group: commands.Group) -> None:
        return await self.send_help_embed(
            "Group Help", group.description, group.commands
        )

    async def send_cog_help(self, cog: commands.Group) -> None:
        return await self.send_help_embed(
            "Category Help", cog.description, cog.get_commands()
        )
