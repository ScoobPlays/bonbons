from disnake.ext import commands
from utils.env import cluster
import disnake

class RPS(disnake.ui.View):
    def __init__(self, ctx, member):
        super().__init__()
        self.ctx = ctx
        self.member = member
        self.author = self.ctx.author
        self.picks = {
            "rock": [],
            "paper": [],
            "scissors": [],
        }

    @disnake.ui.button(label="Rock")
    async def rock(self, button, inter):
        if self.member.id == inter.author.id:
            if self.member.id not in self.picks["rock"]:
                self.picks["rock"].append(self.member.id)
                print(self.picks["rock"])
                await inter.response.send_message(
                    "You chose rock.",
                    ephemeral=True
                )

            else:
                await inter.response.send_message(
                    "You already chose rock!",
                    ephemeral=True
                )
                

        if self.author.id == inter.author.id:
            if self.author.id not in self.picks["rock"]:
                self.picks["rock"].append(self.author.id)
                print(self.picks["rock"])
                await inter.response.send_message(
                    "You chose rock.",
                    ephemeral=True
                )

            else:
                await inter.response.send_message(
                    "You already chose rock!",
                    ephemeral=True
                )

class Development(commands.Cog, description="Commands that are a work in progress."):
    def __init__(self, bot):
        self.bot = bot
        self.afk = cluster["afk"]

    @property
    def cmds(self):
        command = self.bot.cogs["Development"].get_commands()
        return command

    @commands.command()
    async def rps(self, ctx, member: disnake.Member):
        await ctx.send("yeah rps", view=RPS(ctx, member))


def setup(bot):
    bot.add_cog(Development(bot))
