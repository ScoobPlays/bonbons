import contextlib
import disnake
from disnake.ext import commands
from .utils import HelpEmbed

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs = {
                "hidden": True,
                "help": "Shows help about a cog, group or a command"
            }
        )

    async def send(self, **kwargs):
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        embed = HelpEmbed(title="Help Menu")
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

                embed.add_field(
                    name=f"{name} [{amount_commands}]", value=description
                )

        embed.description = f"**About:** bonbons is a bot with no so-many commands.\n**Commands:** There are **{len(self.context.bot.commands)}** commands and **{usable}** of them are usable. There are also **{len(self.context.bot.slash_commands)}** slash commands."

        await self.send(embed=embed)

    async def send_command_help(self, command):
        signature = self.get_command_signature(command).replace(".", "").strip()
        embed = HelpEmbed(
            title=f"`{signature}`", description=command.help or "No help found.."
        )

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases))

        if command._buckets and (
            cooldown := command._buckets._cooldown
        ):
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await self.send(embed=embed)

    async def send_help_embed(
        self, title, description, commands
    ):
        embed = HelpEmbed(title=title, description=description or "No help found..")

        if filtered_commands := await self.filter_commands(commands, sort=True):
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.help or "No help found..",
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