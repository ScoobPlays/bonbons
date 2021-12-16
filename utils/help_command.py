import contextlib
import disnake
from disnake.ext import commands


class HelpEmbed(disnake.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        text = "Use help [command] or help [category] for more information."
        self.set_footer(text=text)
        self.color = disnake.Color.greyple()


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "hidden": True,
                "help": "Shows help about a cog, group or a command",
            }
        )

    async def send(self, **kwargs):
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        embed = HelpEmbed(title="Help Menu").set_footer(
            text="Use help [command] or help [category] for more information.",
            icon_url=self.context.author.display_avatar,
        )
        usable = 0

        for (
            cog,
            commands,
        ) in mapping.items():
            if filtered_commands := await self.filter_commands(commands):
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:
                    name = cog.qualified_name
                    description = cog.description or "No description.."

                embed.add_field(name=f"{name} [{amount_commands}]", value=description)

        embed.description = f"**About:** bonbons is a bot with no so-many commands.\n**Commands:** There are **{len(self.context.bot.commands)}** commands. There are also **{len(self.context.bot.slash_commands)}** slash commands."

        await self.send(embed=embed)

    async def send_command_help(self, command):
        signature = self.get_command_signature(command).replace(".", "").strip()
        embed = HelpEmbed(
            title=f"{signature}", description=command.help or "..."
        ).set_footer(
            text="Use help [command] or help [category] for more information.",
            icon_url=self.context.author.display_avatar,
        )

        embed.add_field(name="Syntax", value=self.get_command_signature(command))
        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases))
        await self.send(embed=embed)

    async def send_help_embed(self, title, description, commands):
        embed = HelpEmbed(title=title, description=description or "...").set_footer(
            text="Use help [command] or help [category] for more information.",
            icon_url=self.context.author.display_avatar,
        )

        if filtered_commands := await self.filter_commands(commands, sort=True):
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.help or "...",
                )

        await self.send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group).replace(".", "").strip()
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "No"
        await self.send_help_embed(
            f"{title} Category", cog.description, cog.get_commands()
        )