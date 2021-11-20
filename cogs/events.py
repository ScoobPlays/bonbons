from disnake import (
    Embed,
    Thread,
    Member,
    User,
    Message,
    Guild,
    Invite,
    ThreadMember,
    Color,
    Forbidden,
    TextChannel,
    VoiceChannel,
    CategoryChannel,
    StoreChannel
    )
from disnake.ext.commands import Cog
import contextlib
from datetime import datetime
from typing import Union

class Events(Cog, description="A cog for events/logs."):
    def __init__(self, bot):
        self.bot = bot
        self.logs = self.bot.get_guild(880030618275155998).get_channel(
            907820956733558784
        )
        self.general = self.bot.get_guild(880030618275155998).get_channel(
            880387280576061450
        )
        self.member = self.bot.get_guild(880030618275155998).get_role(
            880030723908722729
        )

    @Cog.listener()
    async def on_member_join(self, member: Member):

        await self.bot.wait_until_ready()

        if member.guild.id != 880030618275155998:
            return

        await member.add_roles(self.member)
        await self.general.send(
            embed=Embed(
                title="Welcome!",
                description=f"{member.mention} joined! Hope you stay!!",
                color=Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

        embed = Embed(
            title="Member Joined",
            description=f"""
            **Member:** {member} (`{member.id}`)
            **Guild:** {member.guild.name} (`{member.guild.id}`)
            **Joined At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member: Member):

        if member.guild.id != 880030618275155998:
            return

        await self.bot.wait_until_ready()

        await self.general.send(
            embed=Embed(
                title="Goodbye!",
                description=f"{member.mention} left.. :cry:",
                color=Color.green(),
            ).set_footer(text=member, icon_url=member.display_avatar)
        )

        embed = Embed(
            title="Member Removed",
            description=f"""
            **Member:** {member} (`{member.id}`)
            **Guild:** {member.guild.name} (`{member.guild.id}`)
            **Left At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if message.author.bot:
            return

        embed = Embed(
            title="Message Deleted",
            description=f"""
            **Author:** {message.author.mention} (`{message.author.id}`)
            **Guild:** {message.guild.name} (`{message.guild.id}`)
            **Channel:** {message.channel.mention} (`{message.channel.id}`)
            **Deleted At:** <t:{int(message.created_at.timestamp())}:F> (<t:{int(message.created_at.timestamp())}:R>)
            """,
            color=Color.orange(),
        )
        if message.content:
            embed.add_field(name="Message Content", value=message.content)

        if message.attachments:
            embed.set_image(url=message.attachments[0].url)
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before: str, after: str):
        if before.author.bot and after.author.bot:
            return

        embed = (
            Embed(
                title="Message Edited",
                description=f"""
            **Author:** {before.author.mention} (`{before.author.id}`)
            **Guild:** {before.guild.name} (`{before.guild.id}`)
            **Channel:** {before.channel.mention} (`{before.channel.id}`)
            **Deleted At:** <t:{int(before.created_at.timestamp())}:F> (<t:{int(before.created_at.timestamp())}:R>)
            """,
                color=Color.green(),
            )
        )
        if before.content != after.content:
            embed.add_field(name="Before Content", value=before.content, inline=False)
            embed.add_field(name="After Content", value=after.content, inline=False)


        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_create(self, channel: Union[TextChannel, VoiceChannel, CategoryChannel, StoreChannel]):
        embed = Embed(
            title="Channel Created",
            description=f"""
            **Guild:** {channel.guild.name} (`{channel.guild.id}`)
            **Channel:** {channel.name} (`{channel.id}`)
            **Created At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.orange(),
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel: Union[TextChannel, VoiceChannel, CategoryChannel, StoreChannel]):
        embed = Embed(
            title="Channel Deleted",
            description=f"""
            **Guild:** {channel.guild.name} (`{channel.guild.id}`)
            **Channel:** #{channel.name} (`{channel.id}`)
            **Deleted At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.purple(),
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, guild: Guild, user: User):
        embed = Embed(
            title="User Banned",
            description=f"""
            **User:** {user} (`{user.id}`)
            **Guild:** {guild.name} (`{guild.id}`)
            **Banned At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.darker_gray(),
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, guild: Guild, user: User):
        embed = Embed(
            title="User Unbanned",
            description=f"""
            **User:** {user} (`{user.id}`)
            **Guild:** {guild.name} (`{guild.id}`)
            **Unbanned At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.darker_gray(),
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_invite_delete(self, invite: Invite):
        embed = Embed(
            title="Invite Deleted",
            description=f"""
            **Invite:** {invite.code} (`{invite.id}`)
            **Guild:** {invite.guild.name} (`{invite.guild.id}`)
            **Deleted At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.fuchsia(),
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_invite_create(self, invite: Invite):
        embed = Embed(
            title="Invite Created",
            description=f"""
            **Invite:** {invite.code} (`{invite.id}`)
            **Guild:** {invite.guild.name} (`{invite.guild.id}`)
            **Created At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.fuchsia(),
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_thread_join(self, thread: Thread):
        embed = Embed(
            title="Thread Updated",
            description=f"""
            **Thread:** {thread.mention} (`{thread.id}`)
            **Guild:** {thread.guild.name} (`{thread.guild.id}`)
            **Created At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.orange(),
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_thread_delete(self, thread: Thread):
        embed = Embed(
            title="Thread Deleted",
            description=f"""
            **Thread:** #{thread.name} (`{thread.id}`)
            **Guild:** {thread.guild.name} (`{thread.guild.id}`)
            **Deleted At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.orange(),
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_thread_member_join(self, member: ThreadMember):
        member = member.thread.guild.get_member(member.id)
        embed = Embed(
            title="Member Joined a Thread",
            description=f"""
            **Member:** {member.mention} (`{member.id}`)
            **Guild:** {member.guild.name} (`{member.guild.id}`)
            **Joined At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.orange(),
        ).add_field(name="Description", value=f"{member.mention} joined a thread.")
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_thread_member_remove(self, member: ThreadMember):
        member = member.thread.guild.get_member(member.id)
        embed = Embed(
            title="Member Removed from Thread",
            description=f"""
            **Member:** {member.mention} (`{member.id}`)
            **Guild:** {member.guild.name} (`{member.guild.id}`)
            **Removed At:** <t:{int(datetime.utcnow().timestamp())}:F> (<t:{int(datetime.utcnow().timestamp())}:R>)
            """,
            color=Color.orange(),
        ).add_field(
            name="Description", value=f"{member.mention} was removed from a thread."
        )
        await self.logs.send(embed=embed)

    @Cog.listener()
    async def on_message(self, message: Message):

        if message.author.bot:
            return

        if message.author.id in self.bot.cache["afk"].keys():
            del self.bot.cache["afk"][message.author.id]
            await message.channel.send(
                f"Welcome back {message.author.display_name}!",
                delete_after=5.0,
            )
            with contextlib.suppress(Forbidden):
                await message.author.edit(nick=message.author.display_name[6:])

        for mention in message.mentions:
            if msg := self.bot.cache["afk"].get(mention.id):
                await message.channel.send(f"{mention.display_name} is AFK: {msg}")


def setup(bot):
    bot.add_cog(Events(bot))
