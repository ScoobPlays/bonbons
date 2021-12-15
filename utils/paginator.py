import disnake


class Paginator(disnake.ui.View):
    def __init__(self, ctx, messages: list, *, embed: bool):
        super().__init__()
        self.messages = messages
        self.embed = embed
        self.current_page = 0
        self.ctx = ctx

    async def interaction_check(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> bool:
        if inter.author.id != self.ctx.author.id:
            await inter.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False
        return True

    async def show_page(self, inter: disnake.Interaction, page: int):
        if page >= len(self.messages):
            self.current_page = 0
        else:
            self.current_page = page

        self.current.label = f"{self.current_page + 1}/{len(self.messages)}"

        data = self.messages[self.current_page]

        if self.embed:
            await inter.edit_original_message(embed=data, view=self)
        if not self.embed:
            await inter.edit_original_message(content=data, view=self)

    @disnake.ui.button(emoji="⬅️", style=disnake.ButtonStyle.blurple)
    async def back(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @disnake.ui.button(label="Current", style=disnake.ButtonStyle.grey, disabled=True)
    async def current(self, button: disnake.ui.Button, inter: disnake.Interaction):
        pass

    @disnake.ui.button(emoji="➡️", style=disnake.ButtonStyle.blurple)
    async def move(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)

    @disnake.ui.button(label="Quit", style=disnake.ButtonStyle.red)
    async def quit(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await inter.delete_original_message()
