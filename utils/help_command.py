import contextlib
import disnake
from disnake.ext import commands


class HelpCommandSelectOptions(disnake.ui.Select):
    def __init__(
        self, ctx: commands.Context, bot: commands.Bot, embed: disnake.Embed
    ) -> None:
        self.ctx = ctx
        self.bot = bot
        self.embed = embed

        options = []

        for cog in self.bot.cogs:

            cog = self.bot.get_cog(cog)
            if cog.qualified_name in [
                "Jishaku",
                "OnMessage",
                "Owner",
                "MessageCommands",
                "Tasks",
                "Bees",
            ]:
                continue

            options.append(
                disnake.SelectOption(
                    label=cog.qualified_name,
                    description=cog.description,
                    emoji=cog.emoji if cog.emoji else None,
                )
            )
        options.append(
            disnake.SelectOption(
                label="Home", description="Go back to the main help page.", emoji="🏠"
            )
        )

        super().__init__(
            placeholder="Choose a category!",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def get_embed(self, title, description, cmds):
        embed = HelpEmbed(title=title, description=description or "...")
        for command in cmds:
            if isinstance(command, commands.Group):
                for cmd in command.commands:
                    embed.add_field(
                        name=f"{command.name} {cmd.name}", value=cmd.help or "..."
                    )
                embed.add_field(name=command.name, value=command.help)

            if isinstance(command, commands.Command):
                embed.add_field(
                    name=command.name,
                    value=command.help or "...",
                )

        return embed

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()

        if self.values[0] == "Home":
            await interaction.edit_original_message(content=None, embed=self.embed)
            return

        cog = self.bot.get_cog(self.values[0])
        title = cog.qualified_name or "No"

        await interaction.edit_original_message(
            content=None,
            embed=await self.get_embed(
                f"{title} Category", cog.description, cog.get_commands()
            ),
        )


class HelpCommandSelectOption(disnake.ui.View):
    def __init__(self, ctx: commands.Context, bot: commands.Bot, embed):
        super().__init__()
        self.ctx = ctx
        self.bot = bot
        self.embed = embed
        self.add_item(HelpCommandSelectOptions(self.ctx, self.bot, self.embed))

    async def interaction_check(self, interaction) -> bool:
        if interaction.author != self.ctx.author:
            await interaction.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False

        return True


class HelpEmbed(disnake.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = disnake.Color.greyple()


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "hidden": True,
                "help": "Shows help about a category, group or a command",
            }
        )

    async def send(self, **kwargs):
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        prefix = "."

        how2gethelp = f"""
        Use "{prefix}help command" for more info on a command.
        Use "{prefix}help category" for more info on a category.
        Use the dropdown menu below to select a category.
        """

        embed = HelpEmbed(
            title="Bonbons Help Page",
            description=f"Hello! I am bonbons, I was made by {self.context.bot.owner} around <t:1631859987:R>.",
        )
        embed.add_field(name="How do I get help?", value=how2gethelp)

        await self.send(
            embed=embed,
            view=HelpCommandSelectOptions(self.context, self.context.bot, embed),
        )

    async def send_command_help(self, command: commands.Command):
        signature = self.get_command_signature(command).replace(".", "").strip()
        embed = HelpEmbed(title=f"{signature}", description=command.help or "...")

        embed.add_field(name="Syntax", value=self.get_command_signature(command))
        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases))
        await self.send(embed=embed)

    async def send_help_embed(self, title: str, description: str, cmds):
        embed = HelpEmbed(title=title, description=description or "...")
        for command in cmds:
            if isinstance(command, commands.Group):
                for cmd in command.commands:
                    embed.add_field(
                        name=f"{command.name} {cmd.name}", value=cmd.help or "..."
                    )
                embed.add_field(name=command.name, value=command.help)

            if isinstance(command, commands.Command):
                embed.add_field(
                    name=command.name,
                    value=command.help or "...",
                )

        await self.send(embed=embed)

    async def send_cog_help(self, cog):

        title = cog.qualified_name or "No"

        await self.send_help_embed(
            f"{title} Category", cog.description, cog.get_commands()
        )
