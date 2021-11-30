from utils.bonbons import Bonbons
from together import Together
import os
from disnake.ext import commands
import disnake

bot = Bonbons()
client = Together(bot)    

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = disnake.Embed(description=page, color=disnake.Color.greyple())
            await destination.send(embed=embed)

bot.help_command = MyNewHelp()
if __name__ == "__main__":
    bot.run(os.environ["token"])
