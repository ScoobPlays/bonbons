from datetime import timedelta

import disnake
from disnake.ext import tasks
from disnake.ext.commands import Bot, Cog, Context, command

from utils.classes import TimeConverter


class Reminders(
    Cog, description="Reminders that remind you to do something in the future."
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.emoji = "⏲️"
        self.check_for_reminders.start()
        self.base = self.bot.mongo["reminders"]
        self._cached_channels = {}

    async def add_reminder(self, ctx: Context, time: int, reason: str):
        db = self.base[str(ctx.guild.id)]

        await db.insert_one(
            {
                "author": ctx.author.id,
                "time": time,
                "channel": ctx.channel.id,
                "reason": reason,
            }
        )

    @command()
    async def remindme(
        self, ctx: Context, time: TimeConverter, *, reminder: str = None
    ):
        await ctx.send(f"I will remind you in {time} seconds.")
        self._cached_channels[ctx.channel.id] = ctx.channel

        new_time = (disnake.utils.utcnow() + timedelta(seconds=time)).timestamp()
        await self.add_reminder(ctx, int(new_time), reminder)

    @tasks.loop(seconds=10)
    async def check_for_reminders(self):

        await self.bot.wait_until_ready()

        for item in await self.base.list_collections():

            for result in await self.base[item["name"]].find().to_list(100000):
                if int(disnake.utils.utcnow().timestamp()) > result["time"]:
                    collection = self.base[item["name"]]
                    channel = self._cached_channels.get(
                        result["channel"]
                    ) or await self.bot.fetch_channel(result["channel"])

                    member = await self.bot.fetch_user(result["author"])

                    await channel.send(f"Hey {member.mention}, {result['reason']}")

                    await collection.delete_one({"author": result["author"]})


def setup(bot: Bot):
    bot.add_cog(Reminders(bot))
