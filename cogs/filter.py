import disnake
from disnake.ext import commands

banned_words = (
    'stfu',
    'shit bot',
)

class Filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        for word in banned_words:
            if word in message.content:
                await message.reply(
                    file=disnake.File(
                    'utils/assets/gato.png', 'gato.png',)
                    )

def setup(bot):
    bot.add_cog(Filter(bot))