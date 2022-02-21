import random

import discord
from discord.ext import commands

db = {}


class BlackJackButtons(discord.ui.View):
    def __init__(self, ctx: commands.Context, *, bet: int, dealer: int, player: int):
        super().__init__()
        self.ctx = ctx
        self.dealer = dealer
        self.player = player
        self.bet = bet
        self.emoji = "🪙"

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "This command isn't for you.", ephemeral=True
            )
            return False

        return True

    def update_db(self, user: int, *, result: bool) -> None:
        try:
            if result:
                db[user] *= 2
                print(db)
            else:
                db[user] /= 2
                print(db)
        except KeyError:
            db[user] = 10

            if result:
                db[user] *= 2

            else:
                db[user] /= 2

    async def send_embed(
        self, *, result: str, interaction: discord.Interaction, lose: bool = False
    ) -> None:

        await interaction.response.defer()

        embed = discord.Embed(
            title=f"Blackjack ({self.emoji} {self.bet: ,})",
            color=discord.Color.blurple(),
        ).set_author(name=str(self.ctx.author), icon_url=self.ctx.author.display_avatar)

        embed.description = (
            f"Result: {result}\n\nYou: {self.player}\n\nDealer: {self.dealer}"
        )

        if lose:
            for view in self.children:
                view.disabled = True

        await interaction.edit_original_message(view=self, embed=embed)

    async def hit(self, interaction: discord.Interaction):

        id = self.ctx.author.id

        if self.player < 13:
            rng = random.randint(5, 9)
            self.player += rng

            if self.player >= 21:
                await self.send_embed(
                    result="You went over 21!", interaction=interaction, lose=True
                )
                self.update_db(id, result=False)
                return

            if self.player == 21:
                await self.send_embed(
                    result="You won!", interaction=interaction, lose=True
                )
                self.update_db(id, result=True)
                return

            return await self.send_embed(result=f"+ {rng}", interaction=interaction)

        if self.player > 15:
            rng = random.randint(3, 6)
            self.player += rng

            if self.player >= 21:
                await self.send_embed(
                    result="You went over 21!", interaction=interaction, lose=True
                )
                self.update_db(id, result=False)
                return

            if self.player == 21:
                await self.send_embed(
                    result="You won!", interaction=interaction, lose=True
                )
                self.update_db(id, result=True)
                return

            return await self.send_embed(result=f"+ {rng}", interaction=interaction)

    async def start(self):
        embed = discord.Embed(
            title=f"Blackjack ({self.emoji} {self.bet: ,})",
            color=discord.Color.blurple(),
        ).set_author(name=str(self.ctx.author), icon_url=self.ctx.author.display_avatar)

        embed.description = (
            f"Result: Started.\n\nYou: {self.player}\n\nDealer: {self.dealer}"
        )

        await self.ctx.send(embed=embed, view=self)

    @discord.ui.button(label="Hit")
    async def blackjack_hit(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):

        await self.hit(interaction)

    @discord.ui.button(label="Stand")
    async def blackjack_stand(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        ...

    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
    async def blackjack_quit(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):

        await interaction.response.defer()

        for view in self.children:
            view.disabled = True

        await interaction.edit_original_message(view=self)


class Economy(commands.Cog, description="A simple, ephemeral economy system!"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emoji = "🪙"

    def find_or_insert(self, obj: int) -> int:
        data = db.get(obj)

        if data is None:
            money = db[obj] = 10
            return f"{self.emoji} {money}"

        else:
            return f"{self.emoji} {data}"

    @commands.command(aliases=["bal"])
    async def balance(self, ctx: commands.Context):
        """ "Shows your balance"""
        await ctx.send(self.find_or_insert(ctx.author.id))

    @commands.command(aliases=["bj"])
    async def blackjack(self, ctx: commands.Context, bet):

        """
        Bet your money to gain more money!

        """

        if str(bet).startswith("-"):
            return await ctx.reply("Why do you wanna bet on negative money?")

        user = db.get(ctx.author.id)

        if user is None:
            db[user] = 10

        if bet == "all":
            bet = db[user]
            print(bet)

        elif bet > user:
            return await ctx.reply("You cannot bet on money that you don't have.")

        print(type(bet))

        view = BlackJackButtons(
            ctx,
            dealer=random.randint(7, 15),
            player=random.randint(8, 16),
            bet=int(bet),
        )

        await view.start()


def setup(bot):
    bot.add_cog(Economy(bot))
