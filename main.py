from utils.bot import Bonbons
import disnake

bot = Bonbons()

def get_mobile():
    import ast
    import inspect
    import re

    def source(o):
        s = inspect.getsource(o).split("\n")
        indent = len(s[0]) - len(s[0].lstrip())

        return "\n".join(i[indent:] for i in s)

    source_ = source(disnake.gateway.DiscordWebSocket.identify)
    patched = re.sub(
        r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',
        r"\1Discord Android\2",
        source_,
    )

    loc = {}
    exec(compile(ast.parse(patched), "<string>", "exec"), disnake.gateway.__dict__, loc)
    return loc["identify"]


disnake.gateway.DiscordWebSocket.identify = get_mobile()

@bot.event
async def on_message_edit(before: disnake.Message, after: disnake.Message):
    if before.content.startswith((".e", ".eval")):
        await bot.process_commands(a)


bot.run()
