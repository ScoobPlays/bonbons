import discord
import asyncio
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.badwords = ["kayle", "carrot", "geno"]

    def hw_append(self, value):
        self.badwords.append(value)

    @commands.Cog.listener()  # highlights event
    async def on_message(self, msg):

        if msg.author == self.bot.user:
            return

        offsprings = self.bot.get_channel(880030618275156001)

        for word in self.badwords:
            if word in msg.content.lower():
                embed = discord.Embed(
                    title=f'In {msg.guild.name}, "{word}" got highlighted.',
                    description=f"[Jump to message!]({msg.jump_url})",
                )
                embed.add_field(name=f"Message", value=msg.content)
                embed.set_footer(text=f"From {msg.author}")
                await offsprings.send(embed=embed)

    @commands.command()
    async def append(self, ctx, value):

        self.hw_append(value)
        highlights_list = ", ".join(self.badwords)
        embed = discord.Embed(title="Current List", description=f"{highlights_list}")
        await ctx.send(f'Appended "{value}" to the highlights.', embed=embed)

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
            embed=discord.Embed(
                title="Welcome!",
                description=f"{member.mention} joined! Hope you stay!!",
                color=discord.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(880030618275155998)
        channel = guild.get_channel(880387280576061450)

        await channel.send(
            embed=discord.Embed(
                title="Goodbye!",
                description=f"{member.mention} left.. :cry:",
                color=discord.Color.green(),
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
