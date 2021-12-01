import disnake
from urllib.parse import quote_plus
from datetime import datetime

class Google(disnake.ui.View):
    def __init__(self, query: str) -> str:
        super().__init__()
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"
        self.add_item(disnake.ui.Button(label="Click Here", url=url))

class EditSnipeView(disnake.ui.View):
    def __init__(self, ctx, before, after):
        super().__init__()
        self.ctx = ctx
        self.before = before
        self.after = after

    async def interaction_check(self, interaction: disnake.Interaction) -> bool:
        if interaction.user and interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message(
            "You are not the owner of this message.", ephemeral=True
        )
        return False

    @disnake.ui.button(label="Before", style=disnake.ButtonStyle.grey)
    async def before(self, button, inter):

        await inter.response.defer()

        before_embed = (
            disnake.Embed(
                description=f"{self.before.content}",
                timestamp=datetime.utcnow(),
            )
            .set_footer(text=f"Message from {self.before.author}")
            .set_author(
                name=f"{self.before.author}",
                icon_url=self.before.author.display_avatar,
            )
        )

        await inter.edit_original_message(embed=before_embed)

    @disnake.ui.button(label="After", style=disnake.ButtonStyle.grey)
    async def after(self, button, inter):

        await inter.response.defer()

        after_embed = (
            disnake.Embed(
                description=f"{self.after.content}",
                timestamp=datetime.utcnow(),
            )
            .set_footer(text=f"Message from {self.after.author}")
            .set_author(
                name=f"{self.after.author}",
                icon_url=self.after.author.display_avatar,
            )
        )

        await inter.edit_original_message(embed=after_embed)

    @disnake.ui.button(label="Quit", style=disnake.ButtonStyle.red)
    async def quit(self, button, inter):
        await inter.response.defer()
        await inter.delete_original_message()
        await self.ctx.message.delete()

class Calculator(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="1", custom_id="calc:one")
    async def one(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new = data + str(1)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="2", custom_id="calc:two")
    async def two(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new = data + str(2)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="3", custom_id="calc:three")
    async def calc_three(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new = data + str(2)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="+", style=disnake.ButtonStyle.blurple, row=1, custom_id="calc:plus"
    )
    async def plus(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new = data + str("+")
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="=", style=disnake.ButtonStyle.blurple, row=1, custom_id="calc:equals"
    )
    async def equals(self, button, inter):
        await inter.response.defer()
        new = eval(inter.message.content)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="Clear", style=disnake.ButtonStyle.red, row=1, custom_id="calc:clear"
    )
    async def clear(self, button, inter):
        await inter.response.defer()
        await inter.edit_original_message(content="0")
