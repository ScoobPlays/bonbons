import base64
import disnake

async def check(inter, user: disnake.User):
    if inter.author.top_role.position < user.top_role.position:
        return await inter.response.send_message(embed=disnake.Embed(description="You cannot ban a user higher than you.", color=disnake.Color.red()))
    if user == inter.author:
        return await inter.response.send_message(embed=disnake.Embed(description="You cannot ban yourself.", color=disnake.Color.red()))
    if disnake.Forbidden:
        return await inter.response.send_message(embed=disnake.Embed(description="Missing permissions.", color=disnake.Color.red()))

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

def timestamp(value):
    return f"<t:{int(disnake.Object(value).created_at.timestamp())}:F> (<t:{int(disnake.Object(value).created_at.timestamp())}:R>)"
