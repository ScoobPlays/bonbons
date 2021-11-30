from disnake.ext import commands
import disnake


class SelfRoles(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Skilled", style=disnake.ButtonStyle.green, custom_id="green:button"
    )
    async def skilled_button(self, button, inter):
        role = disnake.utils.get(inter.guild.roles, name="Skilled")

        if role in inter.author.roles:
            await inter.response.send_message("Took away the role!", ephemeral=True)
            await inter.author.remove_roles(role)

        if role not in inter.author.roles:
            await inter.response.send_message("Gave you the role!", ephemeral=True)
            await inter.author.add_roles(role)

    @disnake.ui.button(
        label="Experienced", style=disnake.ButtonStyle.red, custom_id="red:button"
    )
    async def experienced_button(self, button, inter):
        role = disnake.utils.get(inter.guild.roles, name="Experienced")

        if role in inter.author.roles:
            await inter.response.send_message("Took away the role!", ephemeral=True)
            await inter.author.remove_roles(role)

        if role not in inter.author.roles:
            await inter.response.send_message("Gave you the role!", ephemeral=True)
            await inter.author.add_roles(role)

    @disnake.ui.button(
        label="Expert", style=disnake.ButtonStyle.blurple, custom_id="blurp:button"
    )
    async def expert_button(self, button, inter):
        role = disnake.utils.get(inter.guild.roles, name="Expert")

        if role in inter.author.roles:
            await inter.response.send_message("Took away the role!", ephemeral=True)
            await inter.author.remove_roles(role)

        if role not in inter.author.roles:
            await inter.response.send_message("Gave you the role!", ephemeral=True)
            await inter.author.add_roles(role)


class Roles(
    commands.Cog, description="A cog for self-roles.", command_attrs=(dict(hidden=True))
):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def selfrole(self, ctx):

        embed = disnake.Embed(title="Self Roles")
        embed.description = "Please pick a role that you like!"
        embed.color = disnake.Color.random()
        await ctx.send(embed=embed, view=SelfRoles())


def setup(bot):
    bot.add_cog(Roles(bot))
