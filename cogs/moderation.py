import disnake
from disnake.ext import commands
from datetime import datetime
from utils.ban import check


class Moderation(commands.Cog, description="Moderation related commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, inter, member: disnake.Member, nickname):
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

    @commands.slash_command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, inter, amount: int = 5):
        """Purges an amount of messages in a channel"""
        await inter.channel.purge(limit=amount)

    @commands.slash_command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter, user: disnake.User, reason=None):
        """Bans a member"""

        await check(inter, user)

        await inter.guild.ban(user, reason=reason)
        embed = disnake.Embed(
            description=f"{user.mention} was banned!",
            color=disnake.Color.red(),
        )
        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, inter, user: disnake.User):
        """Unbans a member"""
        try:
            await inter.guild.fetch_ban(user)
        except disnake.NotFound:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description="That user is not banned.", color=disnake.Color.red()
                )
            )

        embed = disnake.Embed(
            description=f"{user.mention} was unbanned.",
            color=disnake.Color.green(),
        )

        await inter.guild.unban(user)
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
