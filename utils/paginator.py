import disnake
from typing import List

class EmbedPaginator(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0

    async def show_page(self, inter: disnake.ApplicationCommandInteraction, page: int):
        if self.current_page > len(self.embeds):
            self.current_page = 0
        else:
            self.current_page = page
        embed = self.embeds[page]
        await inter.edit_original_message(embed=embed)

    @disnake.ui.button(label="Back", style=disnake.ButtonStyle.blurple)
    async def back(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @disnake.ui.button(label="Next", style=disnake.ButtonStyle.blurple)
    async def move(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)

class Paginator(disnake.ui.View):
    def __init__(self, embeds: List):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0

    async def show_page(self, inter: disnake.ApplicationCommandInteraction, page: int):
        if self.current_page > len(self.embeds):
            self.current_page = 0
        else:
            self.current_page = page
        message = self.embeds[page]
        await inter.edit_original_message(content=message)

    @disnake.ui.button(label="Back", style=disnake.ButtonStyle.blurple)
    async def back(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @disnake.ui.button(label="Next", style=disnake.ButtonStyle.blurple)
    async def move(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)