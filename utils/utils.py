import base64
import disnake
from urllib.parse import quote_plus
import os
import sys

"""Moderation"""


async def check_slash(inter, user: disnake.User):
    if inter.author.top_role.position < user.top_role.position:
        return await inter.response.send_message(
            embed=disnake.Embed(
                description="You cannot ban a user higher than you.",
                color=disnake.Color.red(),
            )
        )
    if user == inter.author:
        return await inter.response.send_message(
            embed=disnake.Embed(
                description="You cannot ban yourself.", color=disnake.Color.red()
            )
        )
    if disnake.Forbidden:
        return await inter.response.send_message(
            embed=disnake.Embed(
                description="Missing permissions.", color=disnake.Color.red()
            )
        )


async def check_ctx(ctx, user: disnake.User):
    if ctx.author.top_role.position < user.top_role.position:
        return await ctx.response.send_message(
            embed=disnake.Embed(
                description="You cannot ban a user higher than you.",
                color=disnake.Color.red(),
            )
        )
    if user == ctx.author:
        return await ctx.response.send_message(
            embed=disnake.Embed(
                description="You cannot ban yourself.", color=disnake.Color.red()
            )
        )
    if disnake.Forbidden:
        return await ctx.response.send_message(
            embed=disnake.Embed(
                description="Missing permissions.", color=disnake.Color.red()
            )
        )


"""Owner"""


def restart_bot():
    os.execv(sys.executable, ["python"] + sys.argv)


def cleanup_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")


def get_syntax_error(e):
    if e.text is None:
        return f"```py\n{e.__class__.__name__}: {e}\n```"
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


def paginate(text: str):
    last = 0
    pages = []

    for curr in range(0, len(text)):
        if curr % 1980 == 0:
            pages.append(text[last:curr])
            last = curr
            appd_index = curr

        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != "", pages))


"""Fun"""


async def b64_encode(text: str):
    message_bytes = text.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    message = base64_bytes.decode("ascii")
    return message


async def b64_decode(text: str):
    b64msg = text.encode("ascii")
    message_bytes = base64.b64decode(b64msg)
    message = message_bytes.decode("ascii")
    return message


class Google(disnake.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"
        self.add_item(disnake.ui.Button(label="Click Here", url=url))


def timestamp(value):
    return f"<t:{int(disnake.Object(value).created_at.timestamp())}:F> (<t:{int(disnake.Object(value).created_at.timestamp())}:R>)"


"""Help Command"""


class HelpEmbed(disnake.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        text = "Use help [command] or help [category] for more information."
        self.set_footer(text=text)
        self.color = disnake.Color.blurple()
