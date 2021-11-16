from disnake.ext import commands
from utils.mongo import starboard, config


class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.starboard_count = 5

    async def set_starboard_count(self, ctx, count):

        """Sets the reactions needed to be on the starboard"""

        data = config.find_one(
            {"reaction_count": "The reaction count for the starboard."}
        )
        values = {"$set": {"reactions": count}}

        config.update_one(data, values)
        await ctx.send(
            f"I have set the reactions needed for the starboard to `{count}`."
        )

        self.starboard_count = count

    async def add_to_starboard(self, reaction, user):
        data = starboard.find_one({"_id": reaction.message.id})

        if data:
            return

        if reaction.message.embeds:
            return

        if not data:
            if reaction.emoji == "⭐" and reaction.count > self.starboard_count:
                await reaction.message.channel.send("Thanks for using this. [WIP]")
                starboard.insert_one(
                    {"_id": reaction.message.id, "author": reaction.message.author.id}
                )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.add_to_starboard(reaction, user)

    @commands.group(invoke_without_command=True)
    async def starboard(self, ctx):
        pass

    @starboard.group(name="set reactions")
    async def _set_reactions(self, ctx, count: int):
        await self.set_starboard_count(ctx, count)


def setup(bot):
    bot.add_cog(Starboard(bot))