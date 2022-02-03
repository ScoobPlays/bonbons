def paginate(text: str) -> None:
    last = 0
    pages = []

    for curr in range(0, len(text)):
        if curr % 1980 == 0:
            pages.append(text[last:curr])
            last = curr
            appd_index = curr

        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != "", pages))


def cleanup_code(content: str) -> str:
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")

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