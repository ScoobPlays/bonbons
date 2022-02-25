import asyncio
import os

from utils.bot import Bonbons


async def main():
    await Bonbons().start()


asyncio.run(main())
