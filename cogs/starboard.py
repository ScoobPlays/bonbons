from disnake.ext import commands
import disnake
from utils.mongo import starboard, config
from datetime import datetime


class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.starboard_count = 5
        self.starboard = self.bot.get_channel(910404322947387422)

    async def set_starboard_count(self, ctx, count):

        """Sets the reactions needed to be on the starboard"""

        try:

            data = await config.find_one(
                {"reaction_count": "The reaction count for the starboard."}
            )
            values = {"$set": {"reactions": count}}

            await config.update_one(data, values)
            await ctx.send(
                f"I have set the reactions needed for the starboard to `{count}`."
            )

            self.starboard_count = count

        except Exception as e:
            print(e)

    async def add_to_starboard(self, reaction, user):

        """Adds something to the starboard (database)"""

        try:

            data = await starboard.find_one({"_id": reaction.message.id})

            if data:
                return

            if reaction.message.embeds:
                return

            if not data:
                if reaction.emoji == "⭐" and reaction.count > self.starboard_count:
                    await self.starboard.send(
                        embed=disnake.Embed(
                            description=reaction.message.content,
                            color=disnake.Color.greyple(),
                            timestamp=datetime.utcnow(),
                        ).set_author(
                            name=reaction.message.author,
                            icon_url=reaction.message.author.display_avatar,
                        )
                    )
                    await starboard.insert_one(
                        {
                            "_id": reaction.message.id,
                            "channel": reaction.message.channel.id,
                            "author": reaction.message.author.id,
                            "content": reaction.message.content

                        }
                    )

        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.add_to_starboard(reaction, user)

    @commands.group(invoke_without_command=True)
    async def starboard(self, ctx):
        """The base command for starboard."""
        await ctx.send_help("starboard")

    @starboard.command()
    @commands.is_owner()
    async def reactions(self, ctx, count: int):
        """Sets the reactions needed for the starboard. (Default is 0)"""
        await self.set_starboard_count(ctx, count)


def setup(bot):
    bot.add_cog(Starboard(bot))
