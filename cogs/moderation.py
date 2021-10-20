import discord
from discord.ext import commands
from datetime import datetime


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["nickname"])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: commands.MemberConverter = None, *, nick):

        if member is None:
            member = ctx.author

        try:
            await member.edit(nick=nick)
            embed = discord.Embed(
                description=f"You have changed {member.mention}'s nick.",
                color=discord.Color.green(),
            )
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

        except Exception:
            embed = discord.Embed(
                description=f"I can't change {member.mention}'s nick.",
                color=discord.Color.red(),
            )
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.display_avatar)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def massnick(self, ctx, *, nick=None):

        embed = discord.Embed(
            title=f"Changing nicknames for {ctx.guild.member_count} members...",
            color=discord.Color.red(),
        )
        send = await ctx.send(embed=embed)

        done = discord.Embed(
            title=f"Changed nicknames for {ctx.guild.member_count} members!",
            color=discord.Color.green(),
        )

        try:
            for member in ctx.guild.members:
                await member.edit(nick=nick)
                print(f"Changing {member}'s nickname...")

        except discord.Forbidden:
            print(f"Couldn't change {member}'s nick.")
            await send.edit(embed=done)
            pass

    @commands.command(
        aliases=["clear", "clean"], help="Purges an amount of messages for you."
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 2):
        await ctx.channel.purge(limit=amount)

    @commands.command(help="A minimal ban comand to ban users.")
    @commands.guild_only()
    @commands.is_owner()
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        await ctx.guild.ban(member, reason=reason)
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"{member.mention} has been banned!",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

    @commands.command(help="A simple unban command to unban users.")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, target: discord.User, *, reason: str = None):
        try:
            await ctx.guild.fetch_ban(target)
        except discord.NotFound:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error", description="That user is not banned."
                )
            )

        embed = discord.Embed(
            title="🛠️ Member Unbanned",
            description=f"{target.mention} has been unbanned!",
            color=discord.Color.green(),
        )

        await ctx.guild.unban(target, reason=reason)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
