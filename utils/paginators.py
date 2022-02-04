from typing import List

from disnake import (ApplicationCommandInteraction, ButtonStyle, Color, Embed,
                     Interaction)
from disnake.ext.commands import Context
from disnake.ui import Button, View, button


class Paginator(View):
    def __init__(
        self, ctx: Context, messages: List, *, embed: bool = False, timeout: int = 60
    ):
        super().__init__(timeout=timeout)
        self.messages = messages
        self.embed = embed
        self.current_page = 0
        self.ctx = ctx

    async def on_timeout(self):
        await self.msg.edit(view=None)

    async def interaction_check(self, inter: ApplicationCommandInteraction) -> bool:
        if inter.author.id != self.ctx.author.id:
            await inter.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False
        return True

    async def show_page(self, inter: Interaction, page: int):
        if page >= len(self.messages):
            self.current_page = 0
        else:
            self.current_page = page

        data = self.messages[self.current_page]

        if self.embed:
            await inter.edit_original_message(embed=data, view=self)
        if not self.embed:
            await inter.edit_original_message(content=data, view=self)

    @button(label="<<", style=ButtonStyle.grey)
    async def back_two(self, button: Button, inter: Interaction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - self.current_page)

    @button(label="Back", style=ButtonStyle.blurple)
    async def back_one(self, button: Button, inter: Interaction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1)

    @button(label="Next", style=ButtonStyle.blurple)
    async def next_one(self, button: Button, inter: Interaction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)

    @button(label="️>>", style=ButtonStyle.grey)
    async def next_two(self, button: Button, inter: Interaction):
        await inter.response.defer()
        await self.show_page(inter, self.current_page - self.current_page - 1)


class MyPages:
    def __init__(self, data):
        self.data = data

    async def start(self, ctx: Context, *, per_page: int):
        embeds = []
        index = 0

        for i in range(0, len(self.data), per_page):
            embed = Embed(
                title="Global Message Leaderboard",
                description="",
                colour=Color.blurple(),
            )
            for user in self.data[i : i + per_page]:
                index += 1
                embed.description += (
                    f"\n{index}. **{user['name']}**: {user['messages']: ,}"
                )

            embeds.append(embed)

        for index, embed in enumerate(embeds):
            index += 1
            embed.set_footer(text=f"Page {index}/{len(embeds)}")

        view = Paginator(ctx, embeds, embed=True)

        view.msg = await ctx.send(embed=embeds[0], view=view)


class TagPages:
    def __init__(self, data):
        self.data = data

    async def start(self, ctx: Context, *, per_page: int):
        embeds = []
        index = 0

        for i in range(0, len(self.data), per_page):
            embed = Embed(
                description="",
                colour=Color.blurple(),
            ).set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
            for result in self.data[i : i + per_page]:
                index += 1
                embed.description += (
                    f"\n{index}. {result['name']} (ID: {result['_id']})"
                )

            embeds.append(embed)

        for index, embed in enumerate(embeds):
            index += 1
            embed.set_footer(
                text=f"Page {index}/{len(embeds)} ({len(self.data)} results)"
            )

        view = Paginator(ctx, embeds, embed=True)

        view.msg = await ctx.send(embed=embeds[0], view=view)


class TextPaginator:
    def __init__(self, ctx: Context, data):
        self.data = data
        self.ctx = ctx

    async def start(self, *, per_page: int = 4000):
        embeds = []

        for index, result in enumerate(self.data):
            embed = Embed(
                description=f"```py\n{result}\n```", color=Color.blurple()
            ).set_footer(text=f"Page {index+1}/{len(self.data)}")
            embeds.append(embed)

        view = Paginator(self.ctx, embeds, embed=True)

        view.msg = await self.ctx.reply(embed=embeds[0], view=view)
