from disnake.ext import commands
from disnake import Embed, Color
from utils.env import starboard, config
from datetime import datetime


class Starboard(commands.Cog, description="Starboard related commands."):
    def __init__(self, bot):
        self.bot = bot

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

        except Exception as e:
            print(e)

    async def add_to_starboard(self, reaction, user):

        """Adds something to the starboard"""

        try:
            if reaction.message.embeds:
                return

            reactions = await config.find_one(
                {"reaction_count": "The reaction count for the starboard."}
            )

            data = await starboard.find_one({"_id": reaction.message.id})
            starboard_channel = self.bot.get_channel(
                910404322947387422
            ) or await self.bot.fetch_channel(910404322947387422)

            if data:
                data_channel = data["channel"]

                msg = self.bot.get_message(
                    data["starboard_message"]
                ) or await self.bot.user.fetch_message(data["starboard_message"])
                await msg.edit(
                    content=f"⭐ **{reaction.count}** <#{data_channel}> ID: {data['_id']}"
                )


            if not data:
                if reaction.emoji == "⭐" and reaction.count > reactions["reactions"]:

                    em = Embed(
                        description=reaction.message.content,
                        color=Color.greyple(),
                        timestamp=datetime.utcnow(),
                    )
                    em.set_author(
                        name=reaction.message.author,
                        icon_url=reaction.message.author.display_avatar,
                    )

                    if reaction.message.attachments:
                        em.set_image(url=reaction.message.attachments[0].url)
                    bot_msg = await starboard_channel.send(
                        content=f"⭐ **{reaction.count}** <#{reaction.message.channel.id}> ID: {reaction.message.id}",
                        embed=em,
                    )
                    await starboard.insert_one(
                        {
                            "_id": reaction.message.id,
                            "channel": reaction.message.channel.id,
                            "author": reaction.message.author.id,
                            "content": reaction.message.content,
                            "starboard_message": bot_msg.id,
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

    @starboard.command()
    async def show(self, ctx, message: int):
        """Shows a message that's been starboard'd"""
        ...


def setup(bot):
    bot.add_cog(Starboard(bot))
