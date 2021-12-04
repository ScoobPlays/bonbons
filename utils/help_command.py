from disnake.ext import commands
import disnake


class HelpEmbed(disnake.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        text = "Use help [command] or help [category] for more information."
        self.set_footer(text=text)
        self.color = disnake.Color.blurple()


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "hidden": True,
                "help": "Shows help about a cog, group or a command",
            }
        )

    def get_ending_note(self, category: bool):
        return f"Use .{self.invoked_with} [{'Category' if category else 'command'}] for more info on {'all commands' if category else 'the command'}"

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

                embed.add_field(name=f"{name} [{amount_commands}]", value=description)
        embed.description = f"**About:** bonbons is a bot with not so-many commands.\n**Commands:** There are **{len(self.context.bot.commands)}** commands and **{usable}** of them are usable. There are also **{len(self.context.bot.slash_commands)}** slash commands."

        await self.send(embed=embed)

    async def send_command_help(self, command):
        desc = command.description
        aliases = command.aliases

        if not aliases:
            aliases = str("...")

        else:
            aliases = ", ".join(aliases)

        em = (
            disnake.Embed(
                title=command.name, description=desc, color=disnake.Color.blurple()
            )
            .add_field(
                name="Syntax",
                value=f"`{self.get_command_signature(command)}`",
                inline=True,
            )
            .add_field(
                name="Aliases",
                value=aliases,
                inline=True,
            )
            .set_author(
                name=self.context.author, icon_url=self.context.author.avatar.url
            )
            .set_footer(
                text=f"Requested by {self.context.author}",
                icon_url=self.context.author.avatar.url,
            )
        )

        await self.send(embed=em)

    async def send_help_embed(self, title, description, commands):
        embed = (
            HelpEmbed(
                title=title,
                description=f"{description}\n\n**Available Subcommands**\n\n",
            )
            .set_author(
                name=self.context.author, icon_url=self.context.author.avatar.url
            )
            .set_footer(
                text=f"Requested by {self.context.author}",
                icon_url=self.context.author.avatar.url,
            )
        )

        if filtered_commands := await self.filter_commands(commands, sort=True):
            for command in filtered_commands:
                embed.description += f"`{command.name}`,"

        await self.send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group).replace(".", "").strip()
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        em = disnake.Embed(
            title=f"{cog.qualified_name} Command's",
            description="",
            color=disnake.Color.blurple(),
        )

        for cmd in cog.get_commands():
            em.description += f"`{cmd.name}`,"

        em.set_author(name=self.context.author, icon_url=self.context.author.avatar.url)
        em.set_footer(
            text=self.get_ending_note(False), icon_url=self.context.author.avatar.url
        )
        await self.send(embed=em)
