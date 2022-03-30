from discord.ext.commands import Cog, Context, command

from utils.bot import Bonbons
import discord

from utils.maze import Maze



class GameView(discord.ui.View):
    def __init__(self, ctx: Context, game: Maze) -> None:
        super().__init__()
        self.game = game
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                f"You are not the owner of this message.",
                ephemeral=True,
            )
            return False
        return True

    def parse_response(self, item: list[list]):
        values = [str(y).replace('0', '⬜').replace('1', '😏').replace('2', '🔳').replace('3', '🟫') for x in item for y in x]
        message = ''

        for i, hi in enumerate(values):
            if i in (2, 5, 8):
                message += f'{hi}\n'
            else:
                message += str(hi)
        
        return message


    @discord.ui.button(label='\u200b', row=0, style=discord.ButtonStyle.blurple, disabled=True)
    async def blank2(self, inter, button):
        pass

    @discord.ui.button(emoji='⬆️', row=0, style=discord.ButtonStyle.blurple)
    async def up(self, inter, button):

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                content=f"You win!",
                view=self
            )
            return

        response = self.game.move_up()

        if 'You' in response:
            await inter.response.send_message(
                response,
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            description=self.parse_response(response)
            )
    
        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                content=f"You win!",
                view=self,
                embed=embed

            )
            return  
        else:
            await inter.response.edit_message(
                embed=embed
            )

    @discord.ui.button(label='\u200b', row=0, style=discord.ButtonStyle.blurple, disabled=True)
    async def blank1(self, inter, button):
        pass

    @discord.ui.button(emoji='⬅️', row=1, style=discord.ButtonStyle.blurple)
    async def left(self, inter, button):

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                content=f"You win!",
                view=self

            )
            return  

        response = self.game.move_left()

        if 'You' in response:
            await inter.response.send_message(
                response,
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            description=self.parse_response(response)
            )

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                content=f"You win!",
                view=self,
                embed=embed

            )
            return  
        else:
            await inter.response.edit_message(
                embed=embed
            )

    @discord.ui.button(emoji='⬇️', row=1, style=discord.ButtonStyle.blurple)
    async def down(self, inter, button):

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                content=f"You win!",
                view=self,
            )
            return  

        response = self.game.move_down()

        if 'You' in response:
            await inter.response.send_message(
                response,
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            description=self.parse_response(response)
            )

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                content=f"You win!",
                view=self,
                embed=embed

            )
            return  
        else:
            await inter.response.edit_message(
                embed=embed
            )

    @discord.ui.button(emoji='➡️', row=1, style=discord.ButtonStyle.blurple)
    async def right(self, inter, button):

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                content=f"You win!",
            )
            return

        response = self.game.move_right()

        if 'You' in response:
            await inter.response.send_message(
                response,
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            description=self.parse_response(response)
            )

        if self.game.check_for_win():

            for item in self.children:
                item.disabled = True

            await inter.response.edit_message(
                content=f"You win!",
                embed=embed,
                view=self

            )
            return  
        else:
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
    async def maze(self, ctx: Context, boxes: int = 4):
        """
        Play a maze game.
        """

        if boxes < 4:
            return await ctx.send('Boxes must be bigger than 4.')

        view = GameView(ctx, Maze(boxes=boxes))
        tree = view.parse_response(view.game.tree)
        embed = discord.Embed(description=tree)
        await ctx.send(embed=embed, view=view)

async def setup(bot: Bonbons):
    await bot.add_cog(Games(bot))