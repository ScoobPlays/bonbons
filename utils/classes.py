import disnake
from disnake.ext import commands
import re

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


class Calculator(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.string = "Click a button!"

    @disnake.ui.button(label="1", custom_id="calc:one")
    async def calc_one(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(1)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="2", custom_id="calc:two")
    async def calc_two(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(2)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="3", custom_id="calc:three")
    async def calc_three(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(3)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="4", row=1, custom_id="calc:four")
    async def calc_four(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(4)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="5", row=1, custom_id="calc:five")
    async def calc_five(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(5)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="6", row=1, custom_id="calc:six")
    async def calc_six(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(6)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="7", row=2, custom_id="calc:seven")
    async def calc_seven(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(7)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="8", row=2, custom_id="calc:eight")
    async def calc_eight(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(8)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(label="9", row=2, custom_id="calc:nine")
    async def calc_nine(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(9)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="+", style=disnake.ButtonStyle.blurple, row=0, custom_id="calc:plus"
    )
    async def plus(self, button, inter):

        if inter.message.content == self.string:
            return await inter.response.send_message(
                "What are you trying to do?", ephemeral=True
            )

        await inter.response.defer()

        data = (inter.message.content).replace(self.string, "")

        new_plus = data.count("+")
        if new_plus >= 1:
            return await inter.response.send_message(
                "You cannot have more than one operator in a message."
            )

        new = data + str("+")
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="*", style=disnake.ButtonStyle.blurple, row=1, custom_id="calc:multiply"
    )
    async def multiply(self, button, inter):
        if inter.message.content == self.string:
            return await inter.response.send_message(
                "What are you trying to do?", ephemeral=True
            )

        await inter.response.defer()

        data = (inter.message.content).replace(self.string, "")
        new_plus = data.count("*")

        if new_plus >= 1:
            return await inter.response.send_message(
                "You cannot have more than one operator in a message."
            )

        new = data + str("*")
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="=", style=disnake.ButtonStyle.blurple, row=2, custom_id="calc:equals"
    )
    async def equals(self, button, inter):
        await inter.response.defer()
        new = eval(inter.message.content)
        await inter.edit_original_message(content=new)

    @disnake.ui.button(
        label="Clear", style=disnake.ButtonStyle.red, row=3, custom_id="calc:clear"
    )
    async def clear(self, button, inter):
        await inter.response.defer()
        await inter.edit_original_message(content="...")

    @disnake.ui.button(
        label="Stop", style=disnake.ButtonStyle.red, row=3, custom_id="calc:stop"
    )
    async def stop(self, button, inter):
        await inter.response.defer()

        for children in self.children:
            children.disabled = True

        await inter.edit_original_message(view=self)


class Advertising(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Support Server", url="https://discord.gg/cJsuVmk8Xq"
            )
        )
        self.add_item(
            disnake.ui.Button(
                label="Invite Me",
                url="https://discordapp.com/oauth2/authorize?client_id=888309915620372491&scope=bot+applications.commands&permissions=0",
            )
        )
