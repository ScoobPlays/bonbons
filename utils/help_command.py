import contextlib
import disnake
from disnake.ext import commands
from .paginators import Paginator


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
                "Owner",
                "Emojis",
                "MessageCommands",
                "Tasks",
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
        self.commands = []
        self.embeds = []

    async def get_embed(self, title, description, cmds):
        for command in cmds:
            if isinstance(command, commands.Group):
                for cmd in command.commands:
                    self.commands.append(
                        {
                            "name": f"{command.name} {cmd.name}",
                            "brief": cmd.help or "...",
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
                    {"name": command.name, "brief": command.description or command.help}
                )

        return self.commands

    async def do_paginate(self, title, desc, data, per_page, inter):

        embeds = []

        for i in range(0, len(data), per_page):
            embed = disnake.Embed(
                title=title,
                description=desc,
                colour=disnake.Color.blurple(),
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

        view = Paginator(self.ctx, self.embeds, timeout=40, embed=True)
        view.add_item(self)

        view.msg = await inter.edit_original_message(
            content=None, embed=self.embeds[0], view=view
        )
        self.embeds = None

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()

        if self.values[0] == "Home":
            await interaction.edit_original_message(content=None, embed=self.embed)
            return

        cog = self.bot.get_cog(self.values[0])
        title = cog.qualified_name or "No"

        await self.do_paginate(
            title,
            cog.description,
            await self.get_embed(title, cog.description, cog.get_commands()),
            10,
            interaction,
        )
        self.commands = []


class HelpCommandSelectOption(disnake.ui.View):
    msg: disnake.Message

    def __init__(self, ctx: commands.Context, bot: commands.Bot, embed):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.bot = bot
        self.embed = embed
        self.add_item(HelpCommandSelectOptions(self.ctx, self.bot, self.embed))

    async def interaction_check(self, interaction: disnake.Interaction) -> bool:
        if interaction.author != self.ctx.author:
            await interaction.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False

        return True

    async def on_timeout(self):
        await self.msg.edit(view=None)


class HelpEmbed(disnake.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = disnake.Color.blurple()


class HelpCommand(commands.HelpCommand):
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

    async def send_bot_help(self, mapping):
        how2gethelp = f"""
        Theres a select menu. Wanna click it?\nAnd if you still want more help, do `help [command]`.\nReplace `[command]` with whatever the command/category/group name is.
        """

        embed = HelpEmbed(
            title="Bonbons Help Page",
            description=f"Hello! I am bonbons, I was made by {self.context.bot.owner} around <t:1631859987:R>.",
        )
        embed.add_field(name="How do I get help?", value=how2gethelp)

        view = HelpCommandSelectOption(self.context, self.context.bot, embed)

        view.msg = await self.send(
            embed=embed,
            view=view,
        )

    async def send_command_help(self, command: commands.Command):
        embed = HelpEmbed(title=command.name, description=command.description or "...")

        embed.add_field(name="Syntax", value=self.get_command_signature(command))
        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases))

        await self.send(embed=embed)

    async def do_paginate(self, title, desc, data, per_page):
        embeds = []

        for i in range(0, len(data), per_page):
            embed = disnake.Embed(
                title=title,
                description=desc,
                colour=disnake.Color.blurple(),
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

    async def send_help_embed(self, title: str, description: str, cmds):
        for command in cmds:
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

        await self.do_paginate(title, description or "...", self.commands, 10)

    async def send_group_help(self, group: commands.Group):
        await self.send_help_embed(group.name, group.description, group.commands)

    async def send_cog_help(self, cog):

        title = cog.qualified_name or "No "

        await self.send_help_embed(
            f"{title} Category", cog.description, cog.get_commands()
        )
