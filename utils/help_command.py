from utils.paginator import EmbedPaginator
from disnake.ext import commands
import disnake


class BonbonsHelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "hidden": True,
                "help": "Shows help about a command, subcommand, group or a cog.",
            }
        )

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = disnake.Embed(description=page, color=disnake.Color.greyple())

            about = disnake.Embed(
                title="About Me",
                description=f"Hello! I am **bonbons**. I am bot with not so-many commands. I have a total of **{len(self.context.bot.commands)}** prefixed commands and **{len(self.context.bot.slash_commands)}** slash commands. I am a private bot made by `kayle#6872` and is made for private use. I am also [on github!](https://github.com/kaylebetter/bonbons) (But the repository is private)",
                color=disnake.Color.greyple(),
            )

            embeds = [embed, about]

            await destination.send(
                embed=embeds[0], view=EmbedPaginator(self.context, embeds)
            )
