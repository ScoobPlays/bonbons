import disnake
from disnake.ext import commands
from datetime import datetime
from disnake import Spotify


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=("av",))
    async def avatar(
        self, ctx, *, member: disnake.Member = None
    ):  # needs slash command

        if member is None:
            member = ctx.author

        embed = disnake.Embed(color=ctx.author.color)
        embed.set_image(url=member.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def serverinfo(self, ctx):

        """Fetches the server's stats"""

        embed = disnake.Embed(
            title=disnake.guild.name,
            description=f"**ID:** {ctx.guild.id}\n**Owner:** {ctx.guild.owner}",
        )
        embed.add_field(
            name="Server Created At",
            value=f"<t:{int(ctx.guild.created_at.timestamp())}:F> (<t:{int(ctx.guild.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Information",
            value=f"• Members: {str(ctx.guild.member_count)}\n• Channels: {len(ctx.guild.channels)}\n• Emojis: {len(ctx.guild.emojis)}\n• Region: {ctx.guild.region}",
        )
        embed.add_field(
            name=f"Server Roles [{len(ctx.guild.roles)}]",
            value=" ".join(r.mention for r in ctx.guild.roles[1:]),
            inline=False,
        )
        embed.timestamp = datetime.utcnow()
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.slash_command(name="serverinfo")
    @commands.guild_only()
    async def serverinfo_slash(self, inter):

        """Fetches the server's stats"""

        embed = disnake.Embed(
            title=disnake.guild.name,
            description=f"**ID:** {inter.guild.id}\n**Owner:** {inter.guild.owner}",
        )
        embed.add_field(
            name="Server Created At",
            value=f"<t:{int(inter.guild.created_at.timestamp())}:F> (<t:{int(inter.guild.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Information",
            value=f"• Members: {str(inter.guild.member_count)}\n• Channels: {len(inter.guild.channels)}\n• Emojis: {len(inter.guild.emojis)}\n• Region: {inter.guild.region}",
        )
        embed.add_field(
            name=f"Server Roles [{len(inter.guild.roles)}]",
            value=" ".join(r.mention for r in inter.guild.roles[1:]),
            inline=False,
        )
        embed.timestamp = datetime.utcnow()
        embed.set_thumbnail(url=inter.guild.icon.url)
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command()
    @commands.guild_only()
    async def membercount_cmd(self, ctx):
        embed = disnake.Embed(
            title="Members",
            description=f"{len(ctx.guild.members)}",
            color=disnake.Color.green(),
        )
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="membercount")
    @commands.guild_only()
    async def membercount_slash(self, inter):
        """Fetches the server member count"""
        embed = disnake.Embed(
            title="Members",
            description=f"{len(inter.guild.members)}",
            color=disnake.Color.green(),
        )
        embed.timestamp = datetime.utcnow()
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(
        aliases=(
            "userinfo",
            "u",
            "ui",
        )
    )
    async def whois(self, ctx, member: disnake.Member = None):  # slash command

        if member is None:
            member = ctx.author

        if len(member.roles) > 1:
            role_string = ", ".join([r.mention for r in member.roles][1:])

        embed = disnake.Embed()
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_author(
            name=f"{member.name}#{member.discriminator}",
            icon_url=f"{member.display_avatar}",
        )
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(
            name="Account Created At",
            value=f"<t:{int(member.created_at.timestamp())}:F> (<t:{int(member.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Joined Server At",
            value=f"<t:{int(member.joined_at.timestamp())}:F> (<t:{int(member.joined_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Roles [{}]\n \n".format(len(member.roles) - 1),
            value=role_string,
            inline=False,
        )
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(help="Fetches information about your spotify activity")
    async def spotify(
        self, ctx: commands.Context, member: disnake.Member = None
    ):  # slash command

        if member is None:
            member = ctx.author

        for activity in member.activities:
            if isinstance(activity, Spotify):
                embed = disnake.Embed(
                    title=f"{member.name}'s Spotify",
                    description=f"**Track ID:** {activity.track_id}",
                )
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Song", value=activity.title)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album, inline=False)
                embed.timestamp = datetime.utcnow()
                embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)

        if not member.activity:
            await ctx.reply("You don't have a spotify activity!", mention_author=False)

    @commands.command(help="Gives you information about a role")
    @commands.guild_only()
    async def roleinfo(
        self, ctx: commands.Context, role: disnake.Role = None
    ):  # slash command

        role_mentionable = None
        role_hoisted = None

        if role is None:
            role = ctx.author.top_role

        x_emoji = "❌"
        check = "✅"

        # Checking to see if some role attributes are false/true

        if role.mentionable is True:
            role_mentionable = check

        if role.hoist is True:
            role_hoisted = check

        if role.mentionable is False:
            role_mentionable = x_emoji

        if role.hoist is False:
            role_hoisted = x_emoji

        embed = disnake.Embed(
            description=f"**Role:** {role.mention}\n**ID:** {role.id}", color=role.color
        )
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.display_avatar}")
        embed.add_field(
            name="Role Created At",
            value=f"<t:{int(role.created_at.timestamp())}:F> (<t:{int(role.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Features",
            value=f"• Color: {role.color}\n• Members: {len(role.members)}\n• Position: {str(role.position)}/{len(ctx.guild.roles)}\n• Hoisted: {role_hoisted}\n• Mentionable: {role_mentionable}",
            inline=False,
        )
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping_cmd(self, ctx):
        """Returns the bots latency"""

        embed = disnake.Embed(
            title="Ponged!", description=f"**Ping:** {round(self.bot.latency * 1000)}ms"
        )

        embed.timestamp = datetime.utcnow()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.slash_command(name="ping")
    async def ping_slash(self, inter):
        """Returns the bots latency"""

        embed = disnake.Embed(
            title="Ponged!", description=f"**Ping:** {round(self.bot.latency * 1000)}ms"
        )

        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
