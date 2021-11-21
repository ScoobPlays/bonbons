import disnake
import aiohttp
from disnake.ext import commands


headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "c8b299ee91msha4c1921cebbedabp1f70a0jsnc4c1cc4b9c5c"
    }

url="https://mashape-community-urban-dictionary.p.rapidapi.com/define"

class Pag(disnake.ui.View):
    def __init__(self, index):
        super().__init__()
        self.index = index
        self.current_page = 1

    async def show_page(self, inter: disnake.ApplicationCommandInteraction, page: int):
        if self.current_page > len(self.index):
            self.current_page = 0
        else:
            self.current_page = page
        msg = self.index[page]
        await inter.edit_original_message(content=msg)

    @disnake.ui.button(label="Back")
    async def back(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @disnake.ui.button(label="Next")
    async def move(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)

class Development(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        
    async def get_urban_response(self, ctx, term):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url, params={"term": term}) as response:
                data = await response.json()
            
                definition = []
                author = []

                for item in data["list"]:
                    definition.append(item['definition'])
                    author.append(item['author'])

                await ctx.send(definition[0], view=Pag(definition))

    @commands.command()
    async def define(self, ctx, term):
        await self.get_urban_response(ctx, term)

def setup(bot):
    bot.add_cog(Development(bot))