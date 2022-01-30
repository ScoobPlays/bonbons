from utils.bot import Bonbons

bot = Bonbons()
bot.blacklist = {}


@bot.event
async def on_message_edit(b, a):

    if b.content.startswith((".e", ".eval")):
        await bot.process_commands(a)


@bot.check
async def blacklist_check(ctx):
    return ctx.author.id not in bot.blacklist.keys()


@bot.command()
async def blacklist(ctx, id: int, reason: str = None):

    if id not in bot.blacklist.keys():
        bot.blacklist[id] = reason if reason else "..."


bot.run()
