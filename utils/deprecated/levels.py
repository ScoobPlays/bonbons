from disnake.ext import commands
from easy_pil import Canvas, Editor, Font, load_image_async
import disnake
import io
import random
import time
from datetime import datetime


class Levels(commands.Cog):
    """A levelling category."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "⬆️"
        self.db = self.bot.mongo["levels"]
        self.levels = {}
        self.base = 125
        self.update_levels()

    def update_levels(self) -> None:
        for item in range(100):
            self.levels[item] = self.base * item

    async def generate_rank_card(
        self, ctx: commands.Context, member: disnake.Member, data, bg=None
    ) -> None:
        next_level_xp = self.levels[int(data["level"]) + 1]
        percentage = (data["xp"] / next_level_xp) * 100
        user_data = {
            "name": str(member),
            "xp": int(data["xp"]),
            "next_level_xp": next_level_xp,
            "level": int(data["level"]),
            "percentage": int(percentage),
        }

        if bg:
            background = Editor(await load_image_async(str(bg))).resize((800, 280))
        else:
            background = Editor(Canvas((800, 280), color="#23272A"))

        profile_image = await load_image_async(str(member.display_avatar.url))
        profile = Editor(profile_image).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

        background.polygon(card_right_shape, "#2C2F33")
        background.paste(profile, (30, 30))

        background.rectangle((30, 200), width=650, height=40, fill="#494b4f", radius=20)
        background.bar(
            (30, 200),
            max_width=650,
            height=40,
            percentage=user_data["percentage"],
            fill="#3db374",
            radius=20,
        )
        background.text((200, 40), user_data["name"], font=poppins, color="white")

        background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
        background.text(
            (200, 130),
            f"Level: {user_data['level']} "
            + f" XP: {user_data['xp']: ,} / {user_data['next_level_xp']: ,}",
            font=poppins_small,
            color="white",
        )

        with io.BytesIO() as img:
            background.save(img, "PNG")
            img.seek(0)

            embed = disnake.Embed(color=disnake.Color.blurple()).set_image(
                file=disnake.File(fp=img, filename="rank.png")
            )
            return await ctx.send(embed=embed)

    async def generate_leaderboard(self, ctx):

        before = time.perf_counter()
        background = Editor(Canvas((1400, 1280), color="#23272A"))
        db = self.db[str(ctx.guild.id)]
        paste_size = 0
        text_size = 40

        for x in await db.find().sort("level", -1).to_list(10):

            user = self.bot.get_user(x["_id"]) or await self.bot.fetch_user(x["_id"])

            if user.avatar is None:
                img = Editor(await load_image_async(str(user.display_avatar))).resize(
                    (128, 128)
                )
            else:
                img = await load_image_async(
                    str(user.display_avatar.with_size(128).with_format("png"))
                )

            background.text(
                (175, text_size),
                f'{str(user)} • Level{x["level"]: ,}',
                color="white",
                font=Font.poppins(size=50),
            )

            background.paste(img, (0, paste_size))
            paste_size += 128
            text_size += 130

        with io.BytesIO() as img:
            background.save(img, "PNG")
            img.seek(0)

            done = time.perf_counter() - before

            embed = disnake.Embed(
                title=f"{ctx.guild.name} Level Leaderboard",
                description="This is based off of your level and not XP.",
                color=disnake.Color.blurple(),
                timestamp=datetime.utcnow(),
            )
            embed.set_image(file=disnake.File(fp=img, filename="leaderboard.png"))
            embed.set_footer(text=f"Took{done: .2f}s")

            return await ctx.send(embed=embed)

    @commands.command(aliases=["level"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.guild_only()
    async def rank(self, ctx: commands.Context, member: disnake.Member = None):
        """Shows your current level in the server."""

        member = member or ctx.author

        db = self.db[str(ctx.guild.id)]

        data = await db.find_one({"_id": member.id})

        if data:
            await self.generate_rank_card(ctx, member, data)

    @commands.command(aliases=["lb"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.guild_only()
    async def leaderboard(self, ctx: commands.Context):
        """Shows the level leaderboard for the current server."""
        await self.generate_leaderboard(ctx)

    @commands.Cog.listener("on_message")
    async def update_xp(self, message: disnake.Message):

        if message.author.bot:
            return

        if not isinstance(message.channel, disnake.TextChannel):
            return

        db = self.db[str(message.guild.id)]

        data = await db.find_one({"_id": message.author.id})
        xp = random.randint(10, 50)

        if data is not None:

            next_level = data["level"] + 1
            next_level_xp = self.levels[next_level]

            if int(data["xp"]) >= int(next_level_xp):
                await db.update_one({"_id": message.author.id}, {"$inc": {"level": 1}})
                await db.update_one(
                    {"_id": message.author.id}, {"$set": {"xp": xp / 2}}
                )
                return

            await db.update_one({"_id": message.author.id}, {"$inc": {"xp": xp}})
            return

        if data is None:
            await db.insert_one({"_id": message.author.id, "xp": xp, "level": 1})
            return


def setup(bot):
    bot.add_cog(Levels(bot))