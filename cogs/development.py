from disnake.ext import commands
from utils.secrets import headers
from utils.secrets import afk as afk_db
from datetime import datetime
import disnake
import aiohttp


url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"


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
    async def back(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @disnake.ui.button(label="Next")
    async def move(
        self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)


class Development(commands.Cog, description="Commands that are a work in progress."):
    def __init__(self, bot):
        self.bot = bot

    async def get_urban_response(self, ctx: commands.Context, term: str):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url, params={"term": term}) as response:
                try:
                    data = await response.json()

                    definition = []

                    for item in data["list"]:
                        definition.append(item["definition"])

                    await ctx.send(definition[0], view=Pag(definition))
                except IndexError:
                    return await ctx.send(
                        embed=disnake.Embed(
                            description="No definitions found for that word.",
                            color=disnake.Color.red(),
                        )
                    )

    @commands.command(aliases=["urban", "meaning"])
    async def define(self, ctx, term):
        """
        Display's a meaning of a word.

        """
        await self.get_urban_response(ctx, term)

    @commands.command()
    async def afk(self, ctx: commands.Context):
        data = await afk_db.find_one({"_id": ctx.author.id})

        if not data:
            await afk_db.insert_one(
                {"_id": ctx.author.id, "timestamp": int(datetime.utcnow().timestamp())}
            )
            await ctx.send("You are now AFK.")
        else:
            return

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):

        if message.author.bot:
            return

        data = await afk_db.find_one({"_id": message.author.id})

        if data:
            await message.channel.send(f"Welcome back {message.author.mention}!")
            await afk_db.delete_one({"_id": message.author.id})

        if message.mentions:
            for member in message.mentions:
                mention_data = await afk_db.find_one({"_id": member.id})
                if mention_data:
                    if member.id == mention_data["_id"]:
                        await message.channel.send(
                            f"{member.mention} is AFK. Since <t:{mention_data['timestamp']}:R>",
                            allowed_mentions=disnake.AllowedMentions(
                                everyone=False, users=False, roles=False
                            ),
                        )
                    else:
                        break
                else:
                    break


def setup(bot):
    bot.add_cog(Development(bot))
