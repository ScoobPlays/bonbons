import disnake

from utils.bot import Bonbons
from utils.objects import get_mobile

bot = Bonbons()

disnake.gateway.DiscordWebSocket.identify = get_mobile()


@bot.event
async def on_message_edit(before: disnake.Message, after: disnake.Message):
    if before.content.startswith((".e", ".eval")):
        await bot.process_commands(after)


bot.run()
