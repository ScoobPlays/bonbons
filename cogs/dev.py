from disnake.ext import commands
from utils.env import headers
from utils.env import cluster
from utils.paginator import EmbedPaginator
from datetime import datetime
from typing import Optional
import disnake
import aiohttp


class Development(commands.Cog, description="Commands that are a work in progress."):
    def __init__(self, bot):
        self.bot = bot
        self.afk = cluster["afk"]

    async def get_urban_response(self, ctx: commands.Context, term: str):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                url="https://mashape-community-urban-dictionary.p.rapidapi.com/define",
                params={"term": term},
            ) as response:
                try:
                    data = await response.json()

                    definition, embeds = [], []

                    for item in data["list"]:
                        definition.append(
                            f'{item["word"]}\n\n**Definition:** {item["definition"]}\n\n**Example:** {item["example"]}\n\n**Author:**\n{item["author"]}'
                        )

                    for name in definition:
                        emb = disnake.Embed(
                            description=name, color=disnake.Color.greyple()
                        )
                        embeds.append(emb)

                    await ctx.send(embed=embeds[0], view=EmbedPaginator(ctx, embeds))
                except IndexError:
                    return await ctx.send(
                        embed=disnake.Embed(
                            description="No definitions found for that word.",
                            color=disnake.Color.red(),
                        )
                    )

    @commands.command(aliases=["urban", "meaning"])
    async def define(self, ctx, term):
        """
        Display's a meaning of a word.

        """
        await self.get_urban_response(ctx, term)

    @commands.command()
    async def afk(self, ctx: commands.Context, reason: Optional[str]):
        """Become AFK."""

        afk_db = self.afk[str(ctx.guild.id)]

        data = await afk_db.find_one({"_id": ctx.author.id})

        if not data:
            if reason:
                await afk_db.insert_one(
                    {
                        "_id": ctx.author.id,
                        "reason": reason,
                        "timestamp": int(datetime.utcnow().timestamp()),
                    }
                )
                await ctx.send(
                    embed=disnake.Embed(
                        description="You are now AFK.", color=ctx.author.top_role.color
                    )
                )
                return

            await afk_db.insert_one(
                {"_id": ctx.author.id, "timestamp": int(datetime.utcnow().timestamp())}
            )
            await ctx.send(
                embed=disnake.Embed(
                    description="You are now AFK.", color=ctx.author.top_role.color
                )
            )
        else:
            return

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if not isinstance(message.channel, disnake.TextChannel):
            return

        if message.author.bot:
            return

        afk_db = self.afk[str(message.guild.id)]

        data = await afk_db.find_one({"_id": message.author.id})

        if data:
            await message.channel.send(
                embed=disnake.Embed(
                    description=f"Welcome back {message.author.mention}!",
                    color=message.author.top_role.color,
                )
            )
            await afk_db.delete_one({"_id": message.author.id})

        if message.mentions:
            for member in message.mentions:
                mention_data = await afk_db.find_one({"_id": member.id})
                if mention_data:
                    if member.id == mention_data["_id"]:
                        if mention_data["reason"]:
                            await message.channel.send(
                                embed=disnake.Embed(
                                    description=f"{member.mention} is AFK: `{mention_data['reason']}` <t:{mention_data['timestamp']}:R>",
                                    color=message.author.top_role.color,
                                ),
                                allowed_mentions=disnake.AllowedMentions(
                                    everyone=False, users=False, roles=False
                                ),
                            )
                        else:
                            await message.channel.send(
                                embed=disnake.Embed(
                                    description=f"{member.mention} is AFK. Since <t:{mention_data['timestamp']}:R>"
                                ),
                                allowed_mentions=disnake.AllowedMentions(
                                    everyone=False, users=False, roles=False
                                ),
                            )
                    else:
                        break
                else:
                    break


def setup(bot):
    bot.add_cog(Development(bot))
