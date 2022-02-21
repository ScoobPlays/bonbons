from utils.bot import Bonbons
import asyncio
import os

async def main():
    await Bonbons().start()

asyncio.run(main())