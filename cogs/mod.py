from datetime import datetime
from typing import Union

import discord
from discord.ext import commands


class Mod(commands.Cog, description="Moderation related commands."):
    def __init__(self, bot):
        self.bot = bot

    @property
    def emoji(self) -> str:
        return "🛠️"

    async def check_ctx(self, ctx, member: discord.Member):

        user = await ctx.guild.fetch_ban(member)

        if user:
            return await ctx.send(
                embed=discord.Embed(
                    description="That user is already banned.",
                    color=discord.Color.red(),
                )
            )

        if member == self.bot.user:
            return await ctx.send(
                embed=discord.Embed(
                    description="I cannot ban myself.", color=discord.Color.red()
                )
            )

        if member == ctx.author:
            return await ctx.send(
                embed=discord.Embed(
                    description="You cannot ban yourself.", color=discord.Color.red()
                )
            )

        if ctx.author.top_role.position < member.top_role.position:
            return await ctx.send(
                embed=discord.Embed(
                    description="You cannot ban a user higher than you.",
                    color=discord.Color.red(),
                )
            )

        else:
            await ctx.guild.ban(user)
            embed = discord.Embed(
                description=f"{user.mention} was banned.",
                color=discord.Color.blurple(),
            )
            await ctx.send(embed=embed)

    async def context_change_name(
        self, ctx: commands.Context, member: discord.Member, nickname: str
    ) -> str:
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                description=f"You have changed {member.mention}'s nick.",
                color=discord.Color.green(),
            )
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

        except Exception:
            embed = discord.Embed(
                description=f"I can't change {member.mention}'s nick.",
                color=discord.Color.red(),
            )
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

    async def interaction_change_nickname(
        self,
        inter: discord.ApplicationCommandInteraction,
        member: discord.Member,
        nickname: str,
    ) -> str:
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                description=f"You have changed {member.mention}'s nick.",
                color=discord.Color.green(),
            )
            embed.set_author(name=str(inter.author), icon_url=inter.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await inter.response.send_message(embed=embed)

        except Exception:
            embed = discord.Embed(
                description=f"I can't change {member.mention}'s nick.",
                color=discord.Color.red(),
            )
            embed.set_author(name=str(inter.author), icon_url=inter.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await inter.response.send_message(embed=embed)

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(
        self, ctx: commands.Context, member: discord.Member, nickname: str
    ) -> str:
        """Change a users nickname"""
        await self.context_change_name(ctx, member, nickname)

    @commands.slash_command(name="nickname")
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname_slash(
        self,
        inter: discord.ApplicationCommandInteraction,
        member: discord.Member,
        nickname: str,
    ):
        """Change a users nickname"""

        await self.interaction_change_nickname(inter, member, nickname)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int = 5):
        """Purges an amount of messages in a channel"""
        await ctx.channel.purge(limit=amount)

    @commands.slash_command(name="purge")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge_slash(
        self, inter: discord.ApplicationCommandInteraction, amount: int = 5
    ):
        """Purges an amount of messages in a channel"""
        x = await inter.channel.purge(limit=amount)
        await inter.response.send_message(f"Purged {len(x)} messages.", ephemeral=True)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: Union[discord.User, discord.Member],
        reason=None,
    ):
        """Bans a member"""

        await self.check_ctx(ctx, user)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
        """Unbans a member"""
        try:
            await ctx.guild.fetch_ban(user)
        except discord.NotFound:
            return await ctx.send(
                embed=discord.Embed(
                    description="That user is not banned or does not exist.",
                    color=discord.Color.blurple(),
                )
            )

        await ctx.guild.unban(user)
        await ctx.send(
            embed=discord.Embed(
                description=f"{user.mention} was unbanned.",
                color=discord.Color.blurple(),
            )
        )


def setup(bot):
    bot.add_cog(Mod(bot))
