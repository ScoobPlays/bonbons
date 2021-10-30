import disnake
from disnake.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Member events
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        guild = self.bot.get_guild(880030618275155998)
        general = guild.get_channel(880387280576061450)
        member_role = guild.get_role(880030723908722729)

        await self.bot.wait_until_ready()

        await member.add_roles(member_role)
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
        if message.author.bot:
            return

        if message.author.id in self.bot.cache["afk"].keys():
            del self.bot.cache["afk"][message.author.id]
            await message.channel.send(
                f"Welcome back {message.author.display_name}!",
                delete_after=4.0,
            )
            with suppress(disnake.Forbidden):
                await message.author.edit(nick=message.author.display_name[6:])
        for mention in message.mentions:
            if msg := self.bot.cache["afk"].get(mention.id):
                await message.channel.send(f"{mention.display_name} is AFK: {msg}")


def setup(bot):
    bot.add_cog(Events(bot))
