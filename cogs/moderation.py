import disnake
from disnake.ext import commands
from datetime import datetime

# needs slash commands


class Moderation(commands.Cog, description="Moderation related commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("nickname",))
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx: commands.Context, member: disnake.Member = None, *, nick):

        if member is None:
            member = ctx.author

        try:
            await member.edit(nick=nick)
            embed = disnake.Embed(
                description=f"You have changed {member.mention}'s nick.",
                color=disnake.Color.green(),
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

        except Exception:
            embed = disnake.Embed(
                description=f"I can't change {member.mention}'s nick.",
                color=disnake.Color.red(),
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.slash_command(name="nickname")
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nick_slash(self, inter, member: disnake.Member, nickname):
        """Change a users nickname"""

        try:
            await member.edit(nick=nickname)
            embed = disnake.Embed(
                description=f"You have changed {member.mention}'s nick.",
                color=disnake.Color.green(),
            )
            embed.set_author(name=inter.author, icon_url=inter.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await inter.response.send_message(embed=embed)

        except Exception:
            embed = disnake.Embed(
                description=f"I can't change {member.mention}'s nick.",
                color=disnake.Color.red(),
            )
            embed.set_author(name=inter.author, icon_url=inter.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await inter.response.send_message(embed=embed)

    @commands.command(
        name="purge",
        aliases=(
            "clear",
            "clean",
        ),
        help="Purges an amount of messages",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge_cmd(self, ctx: commands.Context, amount: int = 2):
        await ctx.channel.purge(limit=amount)

    @commands.slash_command(name="purge")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge_slash(self, inter, amount: int = 2):
        """Purges an amount of messages"""
        await inter.channel.purge(limit=amount)

    @commands.command(help="Bans users")
    @commands.guild_only()
    @commands.is_owner()
    async def ban(self, ctx: commands.Context, member: disnake.Member, *, reason=None):
        await ctx.guild.ban(member, reason=reason)
        embed = disnake.Embed(
            description=f"{member.mention} has been banned!",
            color=disnake.Color.red(),
        )
        await ctx.send(embed=embed)

    @commands.command(help="Unbans users")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(
        self, ctx: commands.Context, target: disnake.User, *, reason: str = None
    ):
        try:
            await ctx.guild.fetch_ban(target)
        except disnake.NotFound:
            return await ctx.send(
                embed=disnake.Embed(description="That user is not banned.")
            )

        embed = disnake.Embed(
            description=f"{target.mention} has been unbanned!",
            color=disnake.Color.green(),
        )

        await ctx.guild.unban(target, reason=reason)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
