import disnake

async def check(inter, user: disnake.User):
    if inter.author.top_role.position < user.top_role.position:
        return await inter.response.send_message(embed=disnake.Embed(description="You cannot ban a user higher than you.", color=disnake.Color.red()))
    if user == inter.author:
        return await inter.response.send_message(embed=disnake.Embed(description="You cannot ban yourself.", color=disnake.Color.red()))
    if disnake.Forbidden:
        return await inter.response.send_message(embed=disnake.Embed(description="Missing permissions.", color=disnake.Color.red()))
