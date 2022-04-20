import asyncio

from utils.bot import Bonbons

bot = Bonbons()


async def main() -> None:
    await bot.start()


asyncio.run(main())
