from discord import Color, Embed


class HelpEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = Color.greyple()
