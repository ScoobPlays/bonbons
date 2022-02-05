def cleanup_code(content: str) -> str:
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")


def get_mobile():
    import ast
    import inspect
    import re

    import disnake

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
