import disnake
from .bonbons import Bot

bot = Bot()

em1 = disnake.Embed(title="First Embed!", color=disnake.Color.green())
em2 = disnake.Embed(title="The Second Embed!", color=disnake.Color.orange())
em3 = disnake.Embed(title="Third Embed!", color=disnake.Color.random())
em4 = disnake.Embed(title="Fourth Embed!", color=disnake.Color.random())
em5 = disnake.Embed(title="Last Embed!", color=disnake.Color.red())

ems = [em1, em2, em3, em4, em5]


@bot.command()
async def pag(ctx):
    current = 0

    class View(disnake.ui.View):
        def __init__(self):
            super().__init__()
            self.current_page = 0


        async def show_page(self, inter, page: int):
            if self.current_page > len(ems):
                self.current_page = 0
            else:
                self.current_page = page
            print(self.current_page)
            embed = ems[page]
            await inter.edit_original_message(embed=embed)

        @disnake.ui.button(label="Back")
        async def back(self, button, inter):
            await inter.response.defer()
            await self.show_page(inter, self.current_page - 1)

        @disnake.ui.button(label="Next")
        async def move(self, button, inter):
            await inter.response.defer()
            await self.show_page(inter, self.current_page + 1)


    await ctx.reply(embed=ems[current], view=View())