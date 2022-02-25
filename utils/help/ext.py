import discord

class HelpEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = discord.Color.greyple()