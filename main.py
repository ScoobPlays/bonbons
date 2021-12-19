from utils.bot import Bonbons
import os, disnake
import utils

bot = Bonbons()


class HelpSelectMenu(disnake.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = []
        
        for cog in bot.cogs:
            cog = bot.get_cog(cog)

            options.append(disnake.SelectOption(
                label=cog.qualified_name, description=cog.description)
                )
        super().__init__(placeholder="pick!",min_values=1,max_values=1,options=options)
        
    async def callback(self, interaction: disnake.MessageInteraction):
        cog = bot.get_cog(self.values[0])
        g = await utils.HelpCommand(self.ctx).get_cog_help(cog)
        await interaction.edit_original_message(g)

class HelpView(disnake.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.add_item(HelpSelectMenu(self.ctx))

@bot.command()
async def b(ctx):
    view = HelpView(ctx)
    await ctx.send('Click an option!', view=view)

if __name__ == "__main__":
    bot.run(os.environ["token"])
