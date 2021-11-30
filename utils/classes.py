import disnake


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
