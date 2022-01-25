from utils.bot import Bonbons
from utils.classes import TimeConverter
from datetime import datetime, timedelta
import disnake
from disnake.ext import tasks

bot = Bonbons()


async def add_reminder(ctx, time, reason):
    db = bot.mongo["reminders"][str(ctx.guild.id)]

    await db.insert_one(
        {"author": ctx.author.id, "time": time, "channel": ctx.channel.id, "reason": reason}
        )


@bot.command()
async def remindme(ctx, time: TimeConverter, reminder: str = None):
    await ctx.send(f"I will remind you in {time} seconds.")

    new_time = (
        disnake.utils.utcnow() + timedelta(seconds=1)
        ).timestamp()
    await add_reminder(ctx, int(new_time), reminder)


@tasks.loop(seconds=10)
async def check_db():

    await bot.wait_until_ready()

    db = bot.mongo["reminders"]

    for item in await db.list_collections():

        for result in await db[item["name"]].find().to_list(100000):
            if int(disnake.utils.utcnow().timestamp()) > result["time"]:
                collection = db[item["name"]]
                channel = await bot.fetch_channel(result["channel"])

                member = await bot.fetch_user(result["author"])

                await channel.send(f"Hey {member.mention}, {result['reason']}")

                await collection.delete_one({"author": result["author"]})

check_db.start()

bot.run()