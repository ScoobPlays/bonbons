from datetime import timedelta
from typing import Dict

import disnake
from disnake.ext import tasks
from disnake.ext.commands import Bot, Cog, Context, command
from utils.classes import TimeConverter


class Reminders(
    Cog, description="Reminders that remind you to do something in the future."
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.emoji: str = "⏲️"
        self.check_for_reminders.start()
        self.base = self.bot.mongo["reminders"]
        self._channels: Dict = {}

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

    @staticmethod
    def parse_time(time: int, *, timestamp: bool = False) -> str:
        data = disnake.utils.utcnow() + timedelta(seconds=time)

        if timestamp:
            return int(data.timestamp())

        return f"<t:{int(data.timestamp())}:F>"

    @command()
    async def remindme(self, ctx: Context, time: TimeConverter, *, reminder: str):

        parsed_time = self.parse_time(time, timestamp=False)
        reminder_time = self.parse_time(time, timestamp=True)
        await ctx.send(f"I will remind you at {parsed_time}.")
        self._channels[ctx.channel.id] = ctx.channel

        await self.add_reminder(ctx, reminder_time, reminder)

    @tasks.loop(seconds=10)
    async def check_for_reminders(self):

        await self.bot.wait_until_ready()

        for item in await self.base.list_collections():

            for result in await self.base[item["name"]].find().to_list(100000):
                if int(disnake.utils.utcnow().timestamp()) > result["time"]:
                    collection = self.base[item["name"]]
                    channel = self._channels.get(
                        result["channel"]
                    ) or await self.bot.fetch_channel(result["channel"])

                    member = f"<@{result['author']}>"

                    await channel.send(f"Hey {member}, {result['reason']}")

                    await collection.delete_one({"author": result["author"]})


def setup(bot: Bot):
    bot.add_cog(Reminders(bot))
