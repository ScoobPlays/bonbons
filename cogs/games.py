from discord.ext.commands import Cog, Context, command

from utils.bot import Bonbons
import discord

from utils.maze import Maze

class GameView(discord.ui.View):
    def __init__(self, ctx, game):
        super().__init__()
        self.game = game
        self.ctx = ctx

    async def interaction_check(self, inter):
        if inter.user.id != self.ctx.author.id:
            await inter.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False
        return True

    def parse_response(self, item: list[list]):
        values = [str(y).replace('0', '⬜').replace('1', '😏').replace('2', '🔳') for x in item for y in x]
        message = ''

        for i, hi in enumerate(s):
            if i in (2, 5, 8):
                message += f'{hi}\n'
            else:
                message += str(hi)
        
        return message

    @discord.ui.button(label='up')
    async def up(self, inter, button):

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                f"You win!",
                view=self,
            )
            return

        response = self.game.move_up()

        if response.startswith('You'):
            await inter.response.send_message(
                response,
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            description=self.parse_response(response)
            )
        await inter.response.edit_message(
            embed=embed
            )
    
    @discord.ui.button(label='down')
    async def down(self, inter, button):

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                f"You win!",
                view=self,
            )
            return  

        response = self.game.move_down()

        if response.startswith('You'):
            await inter.response.send_message(
                response,
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            description=self.parse_response(response)
            )
        await inter.response.edit_message(
            embed=embed
            )

    @discord.ui.button(label='left')
    async def left(self, inter, button):

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                f"You win!",
                view=self,
            )
            return  

        response = self.game.move_left()

        if response.startswith('You'):
            await inter.response.send_message(
                response,
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            description=self.parse_response(response)
            )
        await inter.response.edit_message(
            embed=embed
            )

    @discord.ui.button(label='right')
    async def right(self, inter, button):

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                f"You win!",
                view=self,
            )
            return

        response = self.game.move_right()

        if response.startswith('You'):
            await inter.response.send_message(
                response,
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            description=self.parse_response(response)
            )
        await inter.response.edit_message(
            embed=embed
            )

class Games(Cog):
    """
    Games to play around with.
    """

    def __init__(self, bot: Bonbons) -> None:
        self.bot = bot
    
    @property
    def emoji(self) -> str:
        return "🎮"

    @command(name='maze')
    async def maze(self, ctx: Context, boxes: int = 3):
        """
        Play a maze game.
        """

        view = GameView(ctx, Maze(boxes))
        await ctx.send(content='click the button', view=view)

async def setup(bot: Bonbons):
    await bot.add_cog(Games(bot))