import disnake
from disnake.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Member events
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        guild = self.bot.get_guild(880030618275155998)
        muted_role = guild.get_role(896697171108327475)
        general = guild.get_channel(880387280576061450)
        member_role = guild.get_role(880030723908722729)

        await self.bot.wait_until_ready()
        roles = [member_role, muted_role]

        await member.add_roles(*roles)
        await general.send(
            embed=disnake.Embed(
                title="Welcome!",
                description=f"{member.mention} joined! Hope you stay!!",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        guild = self.bot.get_guild(880030618275155998)
        general = guild.get_channel(880387280576061450)

        await self.bot.wait_until_ready()

        await general.send(
            embed=disnake.Embed(
                title="Goodbye!",
                description=f"{member.mention} left.. :cry:",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

    # Command errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.CommandOnCooldown):
            print(error)
            await ctx.reply(error)

        elif isinstance(error, commands.MissingRequiredArgument):
            print(error)
            await ctx.reply(error)

        else:
            raise error
            await ctx.reply(error)

    # Automod
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        guild = self.bot.get_guild(880030618275155998)
        owner = guild.get_role(884679735366533151)

        if len(message.attachments) > 3:
          
          if owner in message.author.roles:
            return

            await message.delete()
            await message.channel.send(
                f"Too many files! {message.author.mention}", delete_after=7
            )

        if len(message.mentions) > 5:
          
          if owner in message.author.roles:
            print(f"Owner mentioned {message.mentions} people.")
            return

            await message.delete()
            await message.channel.send(
                f"Too many mentions! {message.author.mention}", delete_after=7
            )


def setup(bot):
    bot.add_cog(Events(bot))
