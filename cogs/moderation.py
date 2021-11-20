from disnake import (
    User,
    Color,
    Member,
    Embed,
    ApplicationCommandInteraction,
    NotFound,
    Forbidden
)
from disnake.ext import commands
from datetime import datetime
import asyncio


class Moderation(commands.Cog, description="Moderation related commands."):
    def __init__(self, bot):
        self.bot = bot

    async def check_slash(self, inter, user: User):
        if inter.author.top_role.position < user.top_role.position:
            return await inter.response.send_message(
                embed=Embed(
                    description="You cannot ban a user higher than you.",
                    color=Color.red(),
                ),
                ephemeral=True
            )

        if user == inter.author:
            return await inter.response.send_message(
                embed=Embed(
                    description="You cannot ban yourself.", color=Color.red()
                ),
                ephemeral=True
            )
        if Forbidden:
            return await inter.response.send_message(
                embed=Embed(
                    description="Missing permissions.", color=Color.red()
                ),
                ephemeral=True
            )

    async def check_ctx(self, ctx, user: User):

        if user == ctx.author:
            return await ctx.send(
                embed=Embed(
                    description="You cannot ban yourself.", color=Color.red()
                )
            )
        if Forbidden:
            return await ctx.send(
                embed=Embed(
                    description="Missing permissions.", color=Color.red()
                )
            )

        if ctx.author.top_role.position < user.top_role.position:
            return await ctx.send(
                embed=Embed(
                    description="You cannot ban a user higher than you.",
                    color=Color.red(),
                )
            )

    async def add_mute(self, ctx: commands.Context, member: Member, amount):

        role = utils.get(ctx.guild.roles, name="Muted")

        if not amount:
            return await ctx.send(
                embed=Embed(
                    description="Please provide an amount. (5m, 1h)",
                    color=Color.red(),
                )
            )

        if not role:
            return await ctx.send("No muted role was found.")

        if role in member.roles:
            return await ctx.send(
                embed=Embed(
                    description="Member is already muted.", color=Color.red()
                )
            )

        seconds = amount[:-1]
        dura = amount[-1]
        limit = None
        sleep = None

        if dura == "s":
            limit = "second(s)"
            sleep = int(seconds)

        if dura == "m":
            limit = "minute(s)"
            sleep = int(seconds) * 60

        if dura == "h":
            limit = "hour(s)"
            sleep = int(seconds) * 3600

        await member.add_roles(role)
        await ctx.send(
            embed=Embed(
                description=f"{member.mention} was muted for {seconds} {limit}.",
                color=Color.green(),
            )
        )
        await member.send(
            embed=Embed(
                description=f"You were muted in {ctx.guild.name} for {seconds} {limit}",
                color=Color.red(),
            )
        )
        await asyncio.sleep(sleep)
        await member.remove_roles(role)

    async def remove_mute(self, ctx: commands.Context, member: Member):

        role = ctx.guild.get_role(907560943070896168)

        if role not in member.roles:
            return await ctx.send(
                embed=Embed(
                    description=f"{member.mention} is not muted.",
                    color=Color.green(),
                )
            )

        await member.remove_roles(role)

        await ctx.send(embed=Embed(description=f"Unmuted {member.mention}."))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(
        self,
        ctx: commands.Context,
        member: Member,
        amount,
    ):
        """Mutes a member."""
        await self.add_mute(ctx, member, amount)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx: commands.Context, member: Member):
        """Unmutes a member."""
        await self.remove_mute(ctx, member)

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx: commands.Context, member: Member, nickname):
        """Change a users nickname"""

        try:
            if ctx.author.top_role.position < member.top_role.position:
                return await ctx.send(
                    embed=Embed(
                        description="You cannot change this members nick.",
                        color=Color.red(),
                    )
                )
            await member.edit(nick=nickname)
            embed = Embed(
                description=f"You have changed {member.mention}'s nick.",
                color=Color.green(),
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

        except Exception:
            embed = Embed(
                description=f"I can't change {member.mention}'s nick.",
                color=Color.red(),
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.slash_command(name="nickname")
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname_slash(
        self,
        inter: ApplicationCommandInteraction,
        member: Member,
        nickname,
    ):
        """Change a users nickname"""

        try:
            if inter.author.top_role.position < member.top_role.position:
                return await inter.response.send_message(
                    embed=Embed(
                        description="You cannot change this members nick.",
                        color=Color.red(),
                    ),
                    ephemeral=True,
                )
            await member.edit(nick=nickname)
            embed = Embed(
                description=f"You have changed {member.mention}'s nick.",
                color=Color.green(),
            )
            embed.set_author(name=inter.author, icon_url=inter.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await inter.response.send_message(embed=embed)

        except Exception:
            embed = Embed(
                description=f"I can't change {member.mention}'s nick.",
                color=Color.red(),
            )
            embed.set_author(name=inter.author, icon_url=inter.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await inter.response.send_message(embed=embed)

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
        self, inter: ApplicationCommandInteraction, amount: int = 5
    ):
        """Purges an amount of messages in a channel"""
        x = await inter.channel.purge(limit=amount)
        await inter.response.send_message(f"Purged {len(x)} messages.", ephemeral=True)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: User, reason=None):
        """Bans a member"""

        await self.check_ctx(ctx, user)

        await ctx.guild.ban(user, reason=reason)
        embed = Embed(
            description=f"{user.mention} was banned!",
            color=Color.red(),
        )
        await ctx.send(embed=embed)

    @commands.slash_command(name="ban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban_slash(
        self,
        inter: ApplicationCommandInteraction,
        user: User,
        reason=None,
    ):
        """Bans a member"""

        await self.check_slash(inter, user)
        await inter.guild.ban(user, reason=reason)
        await inter.response.send_message(
            embed=Embed(
                description=f"{user.mention} was banned!", color=Color.red()
            ),
            ephemeral=False,
        )

    @commands.slash_command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban_slash(self, inter, user: User):
        """Unbans a member"""
        try:
            await inter.guild.fetch_ban(user)
        except NotFound:
            return await inter.response.send_message(
                embed=Embed(
                    description="That user is not banned.", color=Color.red()
                ),
                ephemeral=False,
            )

        await inter.guild.unban(user)
        await inter.response.send_message(
            embed=Embed(
                description=f"{user.mention} was unbanned.",
                color=Color.green(),
            ),
            ephemeral=False,
        )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: User):
        """Unbans a member"""
        try:
            await ctx.guild.fetch_ban(user)
        except NotFound:
            return await ctx.send(
                embed=Embed(
                    description="That user is not banned.", color=Color.red()
                )
            )

        await ctx.guild.unban(user)
        await ctx.send(
            embed=Embed(
                description=f"{user.mention} was unbanned.",
                color=Color.green(),
            ),
            ephemeral=False,
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
