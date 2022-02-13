from datetime import datetime

import disnake
from disnake.ext import commands


class Information(commands.Cog, description="Information related commands."):
    def __init__(self, bot):
        self.bot = bot

    @property
    def emoji(self) -> str:
        return "ℹ️"

    @staticmethod
    def created_at(value) -> int:
        obj  = disnake.Object(value)
        return f"<t:{int(obj.created_at.timestamp())}:F> (<t:{int(obj.created_at.timestamp())}:R>)"

    @commands.command()
    async def snowflake(self, ctx: commands.Context, id: int) -> None:

        """Tells you a snowflake's creation date."""

        try:
            embed = disnake.Embed(
                description=f"Snowflake was created at {self.created_at(id)}",
                color=disnake.Color.blurple(),
            )
            await ctx.send(embed=embed)
        except ValueError:
            return await ctx.send(
                embed=disnake.Embed(
                    description="That is not a valid snowflake.",
                    color=disnake.Color.red(),
                )
            )

        else:
            return

    @commands.command(aliases=("av",))
    @commands.guild_only()
    async def avatar(
        self, ctx: commands.Context, *, member: disnake.Member = None
    ) -> None:

        """
        Display's a member's avatar.
        """

        member = member or ctx.author

        embed = disnake.Embed(color=disnake.Color.blurple())
        embed.set_image(url=member.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.slash_command(name="avatar")
    @commands.guild_only()
    async def avatar_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
    ):

        """
        Show's a member's avatar
        """

        member = member or inter.author

        embed = disnake.Embed()
        embed.color = disnake.Color.blurple()
        embed.timestamp = datetime.utcnow()
        
        embed.set_image(url=member.display_avatar)

        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context) -> None:

        """
        Returns information about the current server.
        """

        embed = disnake.Embed(
            title=ctx.guild.name,
            description=f"**ID:** {ctx.guild.id}\n**Owner:** {ctx.guild.owner}",
            color=disnake.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.add_field(
            name="Server Created At",
            value=f"<t:{int(ctx.guild.created_at.timestamp())}:F> (<t:{int(ctx.guild.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Information",
            value=f"• Members: {str(ctx.guild.member_count)}\n• Channels: {len(ctx.guild.channels)}\n• Emojis: {len(ctx.guild.emojis)}",
        )

        if len(str(ctx.guild.roles)) >= 1000:
            embed.add_field(
                name=f"Server Roles [{len(ctx.guild.roles)}]",
                value="There are too many roles to display.",
                inline=False,
            )
        else:
            embed.add_field(
                name=f"Server Roles [{len(ctx.guild.roles)}]",
                value=" ".join(r.mention for r in ctx.guild.roles[::-1]),
                inline=False,
            )

        if ctx.guild.icon is None:
            return await ctx.send(embed=embed)

        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.slash_command(name="serverinfo")
    @commands.guild_only()
    async def serverinfo_slash(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> None:

        """
        Returns information about the current server

        """

        guild = inter.guild

        embed = disnake.Embed(
            title=guild.name,
            description=f"**ID:** {guild.id}\n**Owner:** {guild.owner}",
            color=disnake.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.add_field(
            name="Server Created At",
            value=f"<t:{int(guild.created_at.timestamp())}:F> (<t:{int(guild.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Information",
            value=f"• Members: {str(guild.member_count)}\n• Channels: {len(guild.channels)}\n• Emojis: {len(inter.guild.emojis)}",
        )
        if len(str(guild.roles)) >= 1000:
            embed.add_field(
                name=f"Server Roles [{len(guild.roles)}]",
                value="There are too many roles to display.",
                inline=False,
            )
        else:
            embed.add_field(
                name=f"Server Roles [{len(guild.roles)}]",
                value=" ".join(role.mention for role in guild.roles[::-1]),
                inline=False,
            )

        if guild.icon is None:
            return await inter.response.send_message(embed=embed, ephemeral=False)

        embed.set_thumbnail(url=inter.guild.icon.url)
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command()
    @commands.guild_only()
    async def membercount(self, ctx: commands.Context) -> None:

        """
        Tells you the amount of members in this server.
        """

        embed = disnake.Embed(
            description=f"There are {ctx.guild.member_count} members in **{ctx.guild.name}**.",
            color=disnake.Color.blurple(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def whois(self, ctx: commands.Context, member: disnake.Member = None) -> None:

        """
        Tells you information about a member.
        """

        member = member or ctx.author

        if len(member.roles) > 1:
        roles = " ".join([role.mention for role in member.roles[::-1]])

        embed = disnake.Embed(
            description=f"**Member:** {member.mention}\n**ID:** {member.id}",
            color=disnake.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_author(
            name=member,
            icon_url=member.display_avatar,
        )
        embed.add_field(
            name="Account Created At",
            value=f"{self.created_at(member.id)}",
            inline=False,
        )
        embed.add_field(
            name="Joined Server At",
            value=f"<t:{int(member.joined_at.timestamp())}:F> (<t:{int(member.joined_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name=f"Roles [{len(member.roles)-1}]",
            value=roles,
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.slash_command(name="whois")
    @commands.guild_only()
    async def whois_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
    ) -> None:

        """
        Tell's you information about a member
        """

        member = member or inter.author

        roles = " ".join([role.mention for r in member.roles[::-1]])

        embed = disnake.Embed(
            description=f"**Member:** {member.mention}\n**ID:** {member.id}",
            color=disnake.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_author(
            name=member,
            icon_url=member.display_avatar,
        )
        embed.add_field(
            name="Account Created At",
            value=f"{self.created_at(member.id)}",
            inline=False,
        )
        embed.add_field(
            name="Joined Server At",
            value=f"<t:{int(member.joined_at.timestamp())}:F> (<t:{int(member.joined_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name=f"Roles [{len(member.roles) - 1}]",
            value=roles,
            inline=False,
        )
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command()
    @commands.guild_only()
    async def spotify(
        self, ctx: commands.Context, member: disnake.Member = None
    ) -> None:

        """
        Shows you a member's spotify activity
        """

        member = member or ctx.author

        for activity in member.activities:
            if isinstance(activity, disnake.Spotify):
                embed = disnake.Embed(
                    title=f"{member.name}'s Spotify",
                    description=f"**Track ID:** {activity.track_id}",
                    color=0x1DB954,
                    timestamp=datetime.utcnow(),
                )
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Song", value=activity.title)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album, inline=False)
                embed.set_footer(
                    text=ctx.author, icon_url=ctx.author.display_avatar.url
                )
                await ctx.send(embed=embed)

        if not member.activity:
            await ctx.send("Member does not have a spotify activity.")

    @commands.slash_command(name="spotify")
    @commands.guild_only()
    async def spotify_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
    ) -> None:

        """
        Display a member's spotify activity.
        """

        member = member or inter.author

        if member.activity is None:
            await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"{'You do' if member == inter.author else f'{member.mention} does'} not have a spotify activity.",
                    color=disnake.Color.red(),
                ),
                ephemeral=False,
            )

        for activity in member.activities:
            if isinstance(activity, disnake.Spotify):
                embed = disnake.Embed(
                    title=f"{member.name}'s Spotify",
                    description=f"**Track ID:** {activity.track_id}",
                    color=0x1DB954,
                    timestamp=datetime.utcnow(),
                )
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Song", value=activity.title)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album, inline=False)
                embed.set_footer(
                    text=inter.author, icon_url=inter.author.display_avatar.url
                )
                await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command()
    @commands.guild_only()
    async def roleinfo(self, ctx: commands.Context, role: disnake.Role = None) -> None:

        """
        Tells you information about a role, will use your top role if no role was passed.
        """

        role_mentionable = None
        role_hoisted = None

        role = role or ctx.author.top_role

        x = "❌"
        check = "✅"

        if role.mentionable:
            role_mentionable = check

        if role.hoist is True:
            role_hoisted = check

        if role.mentionable is False:
            role_mentionable = x

        if role.hoist is False:
            role_hoisted = x

        embed = disnake.Embed()
        embed.description = f"**Role:** {role.mention}\n**ID:** {role.id}"
        embed.color = role.color
        embed.timestamp = datetime.utcnow()
        
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
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
        await ctx.send(embed=embed)

    @commands.slash_command(name="roleinfo")
    @commands.guild_only()
    async def roleinfo_slash(
        self, inter: disnake.ApplicationCommandInteraction, role: disnake.Role = None
    ) -> None:

        """
        Tells you information about a role, will use your top role if no role was passed.
        """

        role_mentionable = None
        role_hoisted = None

        role = role or inter.author.top_role

        x_emoji = "❌"
        check = "✅"

        if role.mentionable:
            role_mentionable = check

        if role.hoist is True:
            role_hoisted = check

        if role.mentionable is False:
            role_mentionable = x_emoji

        if role.hoist is False:
            role_hoisted = x_emoji

        embed = disnake.Embed(
            description = f"**Role:** {role.mention}\n**ID:** {role.id}",
            color = role.color,
            timestamp=datetime.utcnow()
            )
        
        embed.set_author(
            name=str(inter.author), icon_url=inter.author.display_avatar
        )
        embed.add_field(
            name="Role Created At",
            value=f"<t:{int(role.created_at.timestamp())}:F> (<t:{int(role.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Features",
            value=f"• Color: {role.color}\n• Members: {len(role.members)}\n• Position: {str(role.position)}/{len(inter.guild.roles)}\n• Hoisted: {role_hoisted}\n• Mentionable: {role_mentionable}",
            inline=False,
        )
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command()
    @commands.guild_only()
    async def channelinfo(self, ctx, channel: disnake.abc.GuildChannel = None):

        """
        Tells you information about a discord channel.
        """

        channel = channel or ctx.channel

        embed = disnake.Embed(
            description=f"**Channel:** {channel.mention}\n**ID:** {channel.id}",
            color=disnake.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar)
        embed.add_field(
            name="Channel Created At",
            value=f"<t:{int(channel.created_at.timestamp())}:F> (<t:{int(channel.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Features",
            value=f"• Category: {channel.category}\n• Position: {channel.position}",
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.slash_command(name="channelinfo")
    @commands.guild_only()
    async def channelinfo_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.abc.GuildChannel = None,
    ):
        """
        Tells you information about a discord channel
        """
        
        channel = channel or inter.channel

        embed = disnake.Embed(
            description=f"**Channel:** {channel.mention}\n**ID:** {channel.id}",
            color=disnake.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.set_author(
            name=inter.author, icon_url=inter.author.display_avatar
        )
        embed.add_field(
            name="Channel Created At",
            value=f"<t:{int(channel.created_at.timestamp())}:F> (<t:{int(channel.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Features",
            value=f"• Category: {channel.category}\n• Position: {channel.position}",
            inline=False,
        )
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))