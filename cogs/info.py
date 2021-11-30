import disnake
from disnake.ext import commands
from datetime import datetime


class Information(commands.Cog, description="Information related commands."):
    def __init__(self, bot):
        self.bot = bot

    def created_at(self, value) -> int:
        return f"<t:{int(disnake.Object(value).created_at.timestamp())}:F> (<t:{int(disnake.Object(value).created_at.timestamp())}:R>)"

    async def context_send_emojis(self, ctx):
        all_emojis = []

        for emoji in ctx.guild.emojis:
            full_emoji = f"<:{emoji.name}:{emoji.id}>"
            all_emojis.append(full_emoji)

        embed = disnake.Embed(
            title=f"Total Emoji's [{len(ctx.guild.emojis)}]",
            description="".join(all_emojis),
            color=disnake.Color.greyple(),
            timestamp=datetime.utcnow(),
        )

        if len(embed) > 2000:
            return await ctx.send("There were too many emoji's. Embed failed to send.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def emojis(self, ctx):
        """Returns all the emojis in the guild."""
        await self.context_send_emojis(ctx)

    @commands.command()
    async def snowflake(self, ctx: commands.Context, argument: int) -> None:

        """Displays a snowflake's creation date."""

        try:
            embed = disnake.Embed(
                description=f"Snowflake was created at {self.created_at(argument)}",
                color=disnake.Color.greyple(),
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

        if member is None:
            member = ctx.author

        embed = disnake.Embed(color=disnake.Color.greyple())
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
        Display's a member's avatar.
        """

        if member is None:
            member = inter.author

        embed = disnake.Embed(
            color=disnake.Color.greyple(), timestamp=datetime.utcnow()
        ).set_image(url=member.display_avatar)

        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context) -> None:

        """
        Returns information about a guild.
        """

        embed = disnake.Embed(
            title=ctx.guild.name,
            description=f"**ID:** {ctx.guild.id}\n**Owner:** {ctx.guild.owner}",
            color=disnake.Color.greyple(),
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
    async def serverinfo_slash(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> None:

        """
        Returns information about a guild.
        """

        embed = disnake.Embed(
            title=inter.guild.name,
            description=f"**ID:** {inter.guild.id}\n**Owner:** {inter.guild.owner}",
            color=disnake.Color.greyple(),
        )
        embed.add_field(
            name="Server Created At",
            value=f"<t:{int(inter.guild.created_at.timestamp())}:F> (<t:{int(inter.guild.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(
            name="Information",
            value=f"• Members: {str(inter.guild.member_count)}\n• Channels: {len(inter.guild.channels)}\n• Emojis: {len(inter.guild.emojis)}",
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
    async def membercount(self, ctx: commands.Context) -> None:

        """
        Returns the amount of members in a guild.
        """

        embed = disnake.Embed(
            description=f"There are {ctx.guild.member_count} members in **{ctx.guild.name}**.",
            color=disnake.Color.greyple(),
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["userinfo"])
    @commands.guild_only()
    async def whois(self, ctx: commands.Context, member: disnake.Member = None) -> None:

        """
        Display's a member's information.
        """

        if member is None:
            member = ctx.author

        if len(member.roles) > 1:
            roles = ", ".join([r.mention for r in member.roles][1:])

        embed = disnake.Embed(
            description=f"**Member:** {member.mention}\n**ID:** {member.id}",
            color=disnake.Color.greyple(),
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
            name="Roles [{}]\n \n".format(len(member.roles) - 1),
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
        Display's a member's information.
        """

        if member is None:
            member = inter.author

        if len(member.roles) > 1:
            role_string = ", ".join([r.mention for r in member.roles][1:])

        embed = disnake.Embed(
            description=f"**Member:** {member.mention}\n**ID:** {member.id}",
            color=disnake.Color.greyple(),
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
            name="Roles [{}]\n \n".format(len(member.roles) - 1),
            value=role_string,
            inline=False,
        )
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command()
    @commands.guild_only()
    async def spotify(
        self, ctx: commands.Context, member: disnake.Member = None
    ) -> None:

        """
        Display a member's spotify activity.
        """

        if member == None:
            member = ctx.author

        for activity in member.activities:
            if isinstance(activity, disnake.Spotify):
                embed = disnake.Embed(
                    title=f"{member.name}'s Spotify",
                    description=f"**Track ID:** {activity.track_id}",
                    color=0x1DB954,
                )
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Song", value=activity.title)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album, inline=False)
                embed.timestamp = datetime.utcnow()
                embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
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

        if member == None:
            member = inter.author

        for activity in member.activities:
            if isinstance(activity, disnake.Spotify):
                embed = disnake.Embed(
                    title=f"{member.name}'s Spotify",
                    description=f"**Track ID:** {activity.track_id}",
                    color=0x1DB954,
                )
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Song", value=activity.title)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album, inline=False)
                embed.timestamp = datetime.utcnow()
                embed.set_footer(
                    text=inter.author, icon_url=inter.author.display_avatar
                )
                await inter.response.send_message(embed=embed, ephemeral=False)

        if not member.activity:
            await inter.response.send_message(
                embed=disnake.Embed(
                    description="Member does not have a spotify activity.",
                    color=disnake.Color.red(),
                ),
                ephemeral=False,
            )

    @commands.command()
    @commands.guild_only()
    async def roleinfo(self, ctx: commands.Context, role: disnake.Role = None) -> None:

        """
        Returns information about a role.
        """

        role_mentionable = None
        role_hoisted = None

        if role == None:
            role = ctx.author.top_role

        x_emoji = "❌"
        check = "✅"

        if role.mentionable is True:
            role_mentionable = check

        if role.hoist is True:
            role_hoisted = check

        if role.mentionable is False:
            role_mentionable = x_emoji

        if role.hoist is False:
            role_hoisted = x_emoji

        embed = disnake.Embed(
            description=f"**Role:** {role.mention}\n**ID:** {role.id}",
            color=role.color,
            timestamp=datetime.utcnow(),
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
        await ctx.send(embed=embed)

    @commands.slash_command(name="roleinfo")
    @commands.guild_only()
    async def roleinfo_slash(
        self, inter: disnake.ApplicationCommandInteraction, role: disnake.Role = None
    ) -> None:

        """
        Returns information about a role.
        """

        role_mentionable = None
        role_hoisted = None

        if role == None:
            role = inter.author.top_role

        x_emoji = "❌"
        check = "✅"

        if role.mentionable is True:
            role_mentionable = check

        if role.hoist is True:
            role_hoisted = check

        if role.mentionable is False:
            role_mentionable = x_emoji

        if role.hoist is False:
            role_hoisted = x_emoji

        embed = disnake.Embed(
            description=f"**Role:** {role.mention}\n**ID:** {role.id}",
            color=role.color,
            timestamp=datetime.utcnow(),
        )
        embed.set_author(
            name=f"{inter.author}", icon_url=f"{inter.author.display_avatar}"
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
        Returns information about a channel.
        """
        if not channel:
            channel = ctx.channel

        embed = disnake.Embed(
            description=f"**Channel:** {channel.mention}\n**ID:** {channel.id}",
            color=disnake.Color.greyple(),
            timestamp=datetime.utcnow(),
        )
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.display_avatar}")
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
    async def channelinfo_slash(self, inter, channel: disnake.abc.GuildChannel = None):
        """
        Returns information about a channel.
        """
        if not channel:
            channel = inter.channel

        embed = disnake.Embed(
            description=f"**Channel:** {channel.mention}\n**ID:** {channel.id}",
            color=disnake.Color.greyple(),
            timestamp=datetime.utcnow(),
        )
        embed.set_author(
            name=f"{inter.author}", icon_url=f"{inter.author.display_avatar}"
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

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:

        """
        Returns the bots latency.
        """

        embed = disnake.Embed(
            description=f"**Ponged!** {self.bot.latency * 1000:.2f}ms",
            color=disnake.Color.greyple(),
        )

        await ctx.reply(embed=embed, mention_author=False)

    @commands.slash_command(name="ping")
    async def ping_slash(self, inter: disnake.ApplicationCommandInteraction) -> None:

        """
        Returns the bots latency
        """

        embed = disnake.Embed(
            description=f"**Ponged!** {self.bot.latency * 1000:.2f}ms",
            color=disnake.Color.greyple(),
        )

        await inter.response.send_message(embed=embed, ephemral=True)


def setup(bot):
    bot.add_cog(Information(bot))
