import disnake
from urllib.parse import quote_plus
import pymongo
from .mongo import cluster

class Google(disnake.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"
        self.add_item(disnake.ui.Button(label="Click Here", url=url))

class HelpEmbed(disnake.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        text = "Use help [command] or help [category] for more information."
        self.set_footer(text=text)
        self.color = disnake.Color.blurple()

def tags_autocomp(inter, input: str) -> str:
    tags = cluster["discord"][str(inter.guild.id)]

    all_tags = []
        
    for tags in tags.find({}):
        all_tags.append(tags["name"])

    return [tag for tag in all_tags if input.lower() in tag]