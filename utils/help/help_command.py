from disnake import Embed, Color
from disnake.ext.commands import HelpCommand, Group, Command
from utils.paginators import Paginator
from .views import HelpCommandMenu
from .ext import HelpEmbed

# TODO:
# Add cleaner typehints
# Better method names

class CustomHelpCommand(HelpCommand):

    """
    A subclassed version of discord.py/disnake's `HelpCommand` class.
    """

    def __init__(self):
        super().__init__(
            command_attrs={
                "hidden": True,
                "help": "Shows help about a category, or a command.",
            }
        )
        self._commands = []

    async def send(self, **kwargs):
        return await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        how2gethelp = f"""
        ```
        help [command]
        help [category]
        help [group]
        ```
        """

        embed = HelpEmbed(
            title="Bonbons Help Page",
            description=f"Hello! I am bonbons, I was made by {self.context.bot.owner} around <t:1631859987:R>.",
        )
        embed.add_field(name="How do I get help?", value=how2gethelp)

        view = HelpCommandMenu(self.context, self.context.bot, embed)

        view.msg = await self.send(
            embed=embed,
            view=view,
        )

    async def send_command_help(self, command: Command):
        embed = HelpEmbed(title="Command Help")
    
        embed.description = f"```\n{self.get_command_signature(command)}\n```\n\n{command.description}"
        

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases))

        await self.send(embed=embed)

    async def paginate(self, title: str, desc: str, data, *, per_page: int):
        embeds = []

        for i in range(0, len(data), per_page):
            embed = Embed(
                title=title,
                description=desc,
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

        view = Paginator(self.context, embeds, embed=True)

        view.msg = await self.send(embed=embeds[0], view=view)

    async def send_help_embed(self, title: str, description: str, _commands):

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
                        "brief": command.description or command.help or "...",
                    }
                )
                break

            if isinstance(command, commands.Command):
                self._commands.append(
                    {
                        "name": command.name,
                        "brief": command.description or command.help or "...",
                    }
                )

        await self.paginate(
            title, description, self._commands, per_page = 7)

    async def send_group_help(self, group: Group):
        await self.send_help_embed(
            "Group Help", group.description, group.commands
        )

    async def send_cog_help(self, cog: Group):
        await self.send_help_embed(
            "Category Help", cog.description, cog.get_commands()
        )
