import disnake
from disnake.ext import commands
from datetime import datetime
from typing import Union

class Moderation(commands.Cog, description="Moderation related commands."):
    def __init__(self, bot):
        self.bot = bot

    async def check_slash(self, inter, user: disnake.User):
        if inter.author.top_role.position < user.top_role.position:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description="You cannot ban a user higher than you.",
                    color=disnake.Color.red(),
                ),
                ephemeral=True
            )

        if user == inter.author:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description="You cannot ban yourself.", color=disnake.Color.red()
                ),
                ephemeral=True
            )
        if disnake.Forbidden:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description="Missing permissions.", color=disnake.Color.red()
                ),
                ephemeral=True
            )

    async def check_ctx(self, ctx, user: disnake.User):

        if user == ctx.author:
            return await ctx.send(
                embed=disnake.Embed(
                    description="You cannot ban yourself.", color=disnake.Color.red()
                )
            )
        if disnake.Forbidden:
            return await ctx.send(
                embed=disnake.Embed(
                    description="Missing permissions.", color=disnake.Color.red()
                )
            )

        if ctx.author.top_role.position < user.top_role.position:
            return await ctx.send(
                embed=disnake.Embed(
                    description="You cannot ban a user higher than you.",
                    color=disnake.Color.red(),
                )
            )

    async def context_change_name(ctx: commands.Context, member: disnake.Member, nickname: str) -> str:
        try:
            if ctx.author.top_role.position < member.top_role.position:
                return await ctx.send(
                    embed=disnake.Embed(
                        description="You cannot change this members nick.",
                        color=disnake.Color.red(),
                    )
                )
            await member.edit(nick=nickname)
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

    async def interaction_change_nickname(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, nickname: str) -> str:
        try:
            if inter.author.top_role.position < member.top_role.position:
                return await inter.response.send_message(
                    embed=disnake.Embed(
                        description="You cannot change this members nick.",
                        color=disnake.Color.red(),
                    ),
                    ephemeral=True,
                )
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

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx: commands.Context, member: disnake.Member, nickname: str) -> str:
        """Change a users nickname"""
        await self.context_change_name(ctx, member, nickname)


    @commands.slash_command(name="nickname")
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
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
        self, inter: disnake.ApplicationCommandInteraction, amount: int = 5
    ):
        """Purges an amount of messages in a channel"""
        x = await inter.channel.purge(limit=amount)
        await inter.response.send_message(f"Purged {len(x)} messages.", ephemeral=True)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: Union[disnake.User, disnake.Member], reason=None):
        """Bans a member"""

        await self.check_ctx(ctx, user)

        await ctx.guild.ban(user, reason=reason)
        embed = disnake.Embed(
            description=f"{user.mention} was banned!",
            color=disnake.Color.red(),
        )
        await ctx.send(embed=embed)

    @commands.slash_command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_slash(
        self,
        inter: disnake.GuildCommandInteraction,
        user: disnake.Member,
        reason=None,
    ):
        """Bans a member"""

        await self.check_slash(inter, user)
        await inter.guild.ban(user, reason=reason)
        await inter.response.send_message(
            embed=disnake.Embed(
                description=f"{user.mention} was banned!", color=disnake.Color.greyple()
            ),
            ephemeral=False,
        )

    @commands.slash_command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban_slash(self, inter: disnake.GuildCommandInteraction, user: disnake.User):
        """Unbans a member"""
        try:
            await inter.guild.fetch_ban(user)
        except disnake.NotFound:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description="That user is not banned.", color=disnake.Color.greyple()
                ),
                ephemeral=False,
            )

        await inter.guild.unban(user)
        await inter.response.send_message(
            embed=disnake.Embed(
                description=f"{user.mention} was unbanned.",
                color=disnake.Color.greyple(),
            ),
            ephemeral=False,
        )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: disnake.User):
        """Unbans a member"""
        try:
            await ctx.guild.fetch_ban(user)
        except disnake.NotFound:
            return await ctx.send(
                embed=disnake.Embed(
                    description="That user is not banned.", color=disnake.Color.greyple()
                )
            )

        await ctx.guild.unban(user)
        await ctx.send(
            embed=disnake.Embed(
                description=f"{user.mention} was unbanned.",
                color=disnake.Color.greyple(),
            ),
            ephemeral=False,
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
