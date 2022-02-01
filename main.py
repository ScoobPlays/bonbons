from utils.bot import Bonbons

bot = Bonbons()


@bot.event
async def on_message_edit(b, a):
    if b.content.startswith((".e", ".eval")):
        await bot.process_commands(a)


bot.run()
