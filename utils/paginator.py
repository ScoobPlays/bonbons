import disnake
from typing import List


class EmbedPaginator(disnake.ui.View):
    def __init__(self, ctx, embeds: List[disnake.Embed]):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0
        self.author = ctx.author

    async def interaction_check(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> bool:
        if inter.author.id != self.author.id:
            await inter.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False
        return True

    async def show_page(self, inter: disnake.ApplicationCommandInteraction, page: int):
        if page >= len(self.embeds):
            self.current_page = 0
        else:
            self.current_page = page
        embed = self.embeds[self.current_page]
        await inter.edit_original_message(embed=embed)

    @disnake.ui.button(label="Back", style=disnake.ButtonStyle.blurple)
    async def back(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @disnake.ui.button(label="Next", style=disnake.ButtonStyle.blurple)
    async def move(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)

    @disnake.ui.button(label="Quit", style=disnake.ButtonStyle.red)
    async def quit(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await inter.delete_original_message()


class Paginator(disnake.ui.View):
    def __init__(self, messages: List):
        super().__init__()
        self.messages = messages
        self.current_page = 0

    async def show_page(self, inter: disnake.ApplicationCommandInteraction, page: int):
        if self.current_page > len(self.messages):
            self.current_page = 0
        else:
            self.current_page = page
        message = self.messages[page]
        await inter.edit_original_message(content=message)

    @disnake.ui.button(label="<<<", style=disnake.ButtonStyle.blurple)
    async def back(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @disnake.ui.button(label=">>>", style=disnake.ButtonStyle.blurple)
    async def move(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)

    @disnake.ui.button(label="Quit", style=disnake.ButtonStyle.red)
    async def quit(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await inter.delete_original_message()
