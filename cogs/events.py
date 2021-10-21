import disnake
from disnake.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(880030618275155998)
        member_role = guild.get_role(880030723908722729)
        muted_role = guild.get_role(896697171108327475)
        channel = guild.get_channel(880387280576061450)

        roles = [member_role, muted_role]

        await member.add_roles(*roles)
        await channel.send(
            embed=disnake.Embed(
                title="Welcome!",
                description=f"{member.mention} joined! Hope you stay!!",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(880030618275155998)
        channel = guild.get_channel(880387280576061450)

        await channel.send(
            embed=disnake.Embed(
                title="Goodbye!",
                description=f"{member.mention} left.. :cry:",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.CommandOnCooldown):  # cd error
            print(error)
            await ctx.reply(error)

        elif isinstance(error, commands.MissingRequiredArgument):
            print(error)
            await ctx.reply(error)

        else:
            print(error)
            await ctx.reply(error)


def setup(bot):
    bot.add_cog(Events(bot))
