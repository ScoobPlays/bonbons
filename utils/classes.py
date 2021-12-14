import disnake
from urllib.parse import quote_plus
from datetime import datetime
from disnake.ext import commands
import re

"""
TimeConvert was stolen from the dpy server, https://discord.com/channels/267624335836053506/343944376055103488/919815774573584414
"""

time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([smhd])")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        matches = time_regex.findall(argument.lower())
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument(
                    "{} is an invalid time-key! h/m/s/d are valid!".format(k)
                )
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


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
        super().__init__()

    @disnake.ui.button(label="1", custom_id="calc:one")
    async def calc_one(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new = data + str(1)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="2", custom_id="calc:two")
    async def calc_two(self, button, inter):
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

    @disnake.ui.button(label="4", row=1, custom_id="calc:four")
    async def calc_four(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new = data + str(4)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="5", row=1, custom_id="calc:five")
    async def calc_five(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new = data + str(5)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="6", row=1, custom_id="calc:six")
    async def calc_six(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new = data + str(6)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="+", style=disnake.ButtonStyle.blurple, row=2, custom_id="calc:plus"
    )
    async def plus(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace("0", "")
        new_plus = data.count("+")
        if new_plus >= 1:
            return
        new = data + str("+")
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="=", style=disnake.ButtonStyle.blurple, row=2, custom_id="calc:equals"
    )
    async def equals(self, button, inter):
        await inter.response.defer()
        new = eval(inter.message.content)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="Clear", style=disnake.ButtonStyle.red, row=2, custom_id="calc:clear"
    )
    async def clear(self, button, inter):
        await inter.response.defer()
        await inter.edit_original_message(content="0")
