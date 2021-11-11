import disnake
from disnake.ext import commands
from datetime import datetime

class Information(commands.Cog, description="Information related commands."):
    def __init__(self, bot):
        self.bot = bot

    def timestamp(self, value):
        return f"<t:{int(disnake.Object(value).created_at.timestamp())}:F> (<t:{int(disnake.Object(value).created_at.timestamp())}:R>)"

    @commands.command()
    async def snowflake(self, ctx: commands.Context, argument: str):

        """Displays a snowflake's creation date"""

        embed = disnake.Embed(
            description=f"Snowflake was created at {self.timestamp(argument)}"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=("av",))
    async def avatar(self, ctx: commands.Context, *, member: disnake.Member = None):

        """
        A command that displays a member's avatar.
        """

        if member is None:
            member = ctx.author

        embed = disnake.Embed(color=ctx.author.color)
        embed.set_image(url=member.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.slash_command(name="avatar")
    async def avatar_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
    ):

        """
        A command that displays a member's avatar.
        """

        if member is None:
            member = inter.author

        embed = disnake.Embed(timestamp=datetime.utcnow()).set_image(
            url=member.display_avatar
        )
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context):

        """
        A command that gets information about a guild. (Needs some permissions)
        """

        embed = disnake.Embed(
            title=ctx.guild.name,
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
    async def serverinfo_slash(self, inter: disnake.ApplicationCommandInteraction):

        """
        A command that gets information about a guild. (Needs some permissions)
        """

        embed = disnake.Embed(
            title=inter.guild.name,
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
    async def membercount(self, ctx: commands.Context):
        """
        A command to display the amount of members in a guild.
        """

        embed = disnake.Embed(
            description=f"`{ctx.guild.member_count}` members in **{ctx.guild.name}**.",
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["userinfo"])
    @commands.guild_only()
    async def whois(self, ctx: commands.Context, member: disnake.Member = None):

        """
        A command to display a member's information.
        """

        if member is None:
            member = ctx.author

        if len(member.roles) > 1:
            role_string = ", ".join([r.mention for r in member.roles][1:])

        embed = disnake.Embed(timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_author(
            name=member,
            icon_url=member.display_avatar,
        )
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(
            name="Account Created At", value=f"{self.timestamp(member.id)}", inline=False
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
        await ctx.send(embed=embed)

    @commands.slash_command(name="whois")
    @commands.guild_only()
    async def whois_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
    ):

        """
        A command to display a member's information.
        """

        if member is None:
            member = inter.author

        if len(member.roles) > 1:
            role_string = ", ".join([r.mention for r in member.roles][1:])

        embed = disnake.Embed(timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_author(
            name=member,
            icon_url=member.display_avatar,
        )
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(
            name="Account Created At", value=f"{self.timestamp(member.id)}", inline=False
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
    async def spotify(self, ctx: commands.Context, member: disnake.Member = None):

        """
        A command to display a member's spotify activity.
        """

        if member == None:
            member = ctx.author

        for activity in member.activities:
            if isinstance(activity, disnake.Spotify):
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
            await ctx.send("Member does not have a spotify activity.")

    @commands.slash_command(name="spotify")
    async def spotify_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
    ):

        """
        A command to display a member's spotify activity.
        """

        if member == None:
            member = inter.author

        for activity in member.activities:
            if isinstance(activity, disnake.Spotify):
                embed = disnake.Embed(
                    title=f"{member.name}'s Spotify",
                    description=f"**Track ID:** {activity.track_id}",
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
                "Member does not have a spotify activity.", ephemeral=False
            )

    @commands.command()
    @commands.guild_only()
    async def roleinfo(self, ctx: commands.Context, role: disnake.Role = None):

        """
        A command to display a roles' stats.
        If no arguments were passed the author's top role will be taken as the role.
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
    ):

        """
        A command to display a roles' information.
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

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):

        """
        Returns the bots latency
        """

        embed = disnake.Embed(
            description=f"**Pinged!** {round(self.bot.latency * 1000)}ms"
        )

        await ctx.reply(embed=embed, mention_author=False)

    @commands.slash_command(name="ping")
    async def ping_slash(self, inter: disnake.ApplicationCommandInteraction):

        """
        Returns the bots latency
        """

        embed = disnake.Embed(
            description=f"**Pinged!** {round(self.bot.latency * 1000)}ms"
        )

        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
