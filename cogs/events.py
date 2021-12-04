import disnake
from disnake.ext.commands import Cog
from datetime import datetime


class Events(Cog, description="A cog for events/logs."):
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, embed: disnake.Embed):
        name = "Bonbons Logs"
        channel = self.bot.get_channel(
            907820956733558784
        ) or await self.bot.fetch_channel(907820956733558784)

        webhooks = await channel.webhooks()
        webhook = disnake.utils.find(lambda w: w.name == name, webhooks)

        await webhook.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        if before.roles != after.roles:
            embed = disnake.Embed(
                title="Member Updated",
                description=f"""
                **Member:** {before.mention} (`{before.id}`)
                **Guild:** {before.guild.name} (`{before.guild.id}`)
                **Changed At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
                """,
                color=disnake.Color.greyple(),
            )
            embed.add_field(
                name=f"Old Roles",
                value=" ".join([role.mention for role in before.roles[1:]]),
            )
            embed.add_field(
                name=f"New Roles",
                value=" ".join([role.mention for role in after.roles[1:]]),
            )
            await self.send_log(embed=embed)

        if before.display_name != after.display_name:
            embed = disnake.Embed(
                title="Member Updated",
                description=f"""
                **Member:** {before.mention} (`{before.id}`)
                **Guild:** {before.guild.name} (`{before.guild.id}`)
                **Changed At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
                """,
                color=disnake.Color.greyple(),
            )
            embed.add_field(name="Old Nickname", value=before.display_name)
            embed.add_field(name="New Nickname", value=after.display_name)
            await self.send_log(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member: disnake.Member):

        await self.bot.wait_until_ready()

        if member.guild.id != 880030618275155998:
            return

        general = self.bot.get_channel(
            880387280576061450
        ) or await self.bot.fetch_channel(880387280576061450)

        guild = self.bot.get_guild(880030618275155998) or await self.bot.fetch_guild(
            880030618275155998
        )

        member = guild.get_role(880030723908722729)

        await member.add_roles(member)
        await general.send(
            embed=disnake.Embed(
                title="Welcome!",
                description=f"{member.mention} joined! Hope you stay!!",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

        embed = disnake.Embed(
            title="Member Joined",
            description=f"""
            **Member:** {member} (`{member.id}`)
            **Guild:** {member.guild.name} (`{member.guild.id}`)
            **Joined At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member: disnake.Member):

        await self.bot.wait_until_ready()

        if member.guild.id != 880030618275155998:
            return

        general = self.bot.get_channel(
            880387280576061450
        ) or await self.bot.fetch_channel(880387280576061450)

        await general.send(
            embed=disnake.Embed(
                title="Goodbye!",
                description=f"{member.mention} left.. :cry:",
                color=disnake.Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

        embed = disnake.Embed(
            title="Member Removed",
            description=f"""
            **Member:** {member} (`{member.id}`)
            **Guild:** {member.guild.name} (`{member.guild.id}`)
            **Left At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if message.author.bot:
            return

        embed = disnake.Embed(
            title="Message Deleted",
            description=f"""
            **Author:** {message.author.mention} (`{message.author.id}`)
            **Guild:** {message.guild.name} (`{message.guild.id}`)
            **Channel:** {message.channel.mention} (`{message.channel.id}`)
            **Deleted At:** <t:{int(message.created_at.timestamp())}:F> (<t:{int(message.created_at.timestamp())}:R>)
            """,
            color=disnake.Color.orange(),
        )
        if message.content:
            embed.add_field(name="Message Content", value=message.content)

        if message.attachments:
            embed.set_image(url=message.attachments[0].url)
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):

        if before.author.bot and after.author.bot:
            return

        embed = disnake.Embed(
            title="Message Edited",
            description=f"""
            **Author:** {before.author.mention} (`{before.author.id}`)
            **Guild:** {before.guild.name} (`{before.guild.id}`)
            **Channel:** {before.channel.mention} (`{before.channel.id}`)
            **Edited At:** <t:{int(before.created_at.timestamp())}:F> (<t:{int(before.created_at.timestamp())}:R>)
            """,
            color=disnake.Color.greyple(),
        )
        if before.content != after.content:
            embed.add_field(name="Before Content", value=before.content, inline=False)
            embed.add_field(name="After Content", value=after.content, inline=False)

            await self.send_log(embed=embed)

    @Cog.listener()
    async def on_guild_channel_create(self, channel: disnake.abc.GuildChannel):
        embed = disnake.Embed(
            title="Channel Created",
            description=f"""
            **Guild:** {channel.guild.name} (`{channel.guild.id}`)
            **Channel:** {channel.mention} (`{channel.id}`)
            **Created At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.brand_green(),
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel: disnake.abc.GuildChannel):
        embed = disnake.Embed(
            title="Channel Deleted",
            description=f"""
            **Guild:** {channel.guild.name} (`{channel.guild.id}`)
            **Channel:** #{channel.name} (`{channel.id}`)
            **Deleted At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.brand_green(),
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, guild: disnake.Guild, user: disnake.User):
        embed = disnake.Embed(
            title="User Banned",
            description=f"""
            **User:** {user} (`{user.id}`)
            **Guild:** {guild.name} (`{guild.id}`)
            **Banned At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.darker_gray(),
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, guild: disnake.Guild, user: disnake.User):
        embed = disnake.Embed(
            title="User Unbanned",
            description=f"""
            **User:** {user} (`{user.id}`)
            **Guild:** {guild.name} (`{guild.id}`)
            **Unbanned At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.darker_gray(),
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_invite_delete(self, invite: disnake.Invite):
        embed = disnake.Embed(
            title="Invite Deleted",
            description=f"""
            **Invite:** {invite.code} (`{invite.id}`)
            **Guild:** {invite.guild.name} (`{invite.guild.id}`)
            **Deleted At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.fuchsia(),
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_invite_create(self, invite: disnake.Invite):
        embed = disnake.Embed(
            title="Invite Created",
            description=f"""
            **Invite:** {invite.code} (`{invite.id}`)
            **Guild:** {invite.guild.name} (`{invite.guild.id}`)
            **Created At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.fuchsia(),
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_thread_join(self, thread: disnake.Thread):
        embed = disnake.Embed(
            title="Thread Updated",
            description=f"""
            **Thread:** {thread.mention} (`{thread.id}`)
            **Guild:** {thread.guild.name} (`{thread.guild.id}`)
            **Created At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.orange(),
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_thread_delete(self, thread: disnake.Thread):
        embed = disnake.Embed(
            title="Thread Deleted",
            description=f"""
            **Thread:** #{thread.name} (`{thread.id}`)
            **Guild:** {thread.guild.name} (`{thread.guild.id}`)
            **Deleted At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.orange(),
        )
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_thread_member_join(self, member: disnake.ThreadMember):
        member = member.thread.guild.get_member(member.id)
        embed = disnake.Embed(
            title="Member Joined a Thread",
            description=f"""
            **Member:** {member.mention} (`{member.id}`)
            **Guild:** {member.guild.name} (`{member.guild.id}`)
            **Joined At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.orange(),
        ).add_field(name="Description", value=f"{member.mention} joined a thread.")
        await self.send_log(embed=embed)

    @Cog.listener()
    async def on_thread_member_remove(self, member: disnake.ThreadMember):
        member = member.thread.guild.get_member(member.id)
        embed = disnake.Embed(
            title="Member Removed from Thread",
            description=f"""
            **Member:** {member.mention} (`{member.id}`)
            **Guild:** {member.guild.name} (`{member.guild.id}`)
            **Removed At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=disnake.Color.orange(),
        ).add_field(
            name="Description", value=f"{member.mention} was removed from a thread."
        )
        await self.send_log(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
