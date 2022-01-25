from typing import Union, Optional
from pyston import PystonClient, File
from disnake.ext import commands
import disnake
import utils
import re
import asyncio
from datetime import datetime
import googletrans


class Helpful(commands.Cog):
    """Commands that may be helpful?"""

    def __init__(self, bot):
        self.pysclient = PystonClient()
        self.CODE_REGEX = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")
        self.bot = bot
        self.emoji = "🫂"
        self.db = self.bot.mongo["discord"]["bot"]
        self.RUN_CACHE = {}
        self.msg = self.bot.mongo["discord"]["messages"]
        self.trans = googletrans.Translator()

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        tag = await self.db.find_one({"_id": self.bot.user.id})

        if not tag:
            await self.db.insert_one({"_id": self.bot.user.id, "uses": 0})

        uses = tag["uses"] + 1

        await self.db.update_one(tag, {"$set": {"uses": int(uses)}})

        self.bot.LAST_COMMANDS_USAGE.append(
            {"mention": ctx.author, "timestamp": int(datetime.utcnow().timestamp())}
        )
        self.bot.invoked_commands = uses

    def created_at(self, value):
        return f"<t:{int(disnake.Object(value).created_at.timestamp())}:F> (<t:{int(disnake.Object(value).created_at.timestamp())}:R>)"

    async def run_code(self, ctx: commands.Context, lang: str, code: str) -> None:
        matches = self.CODE_REGEX.findall(code)

        try:
            lang = lang.split("```")[1]
            code = code.split("```")[0]
            output = await self.pysclient.execute(str(lang), [File(code)])

            if (
                output.raw_json["run"]["stdout"] == ""
                and output.raw_json["run"]["stderr"]
            ):
                self.RUN_CACHE[ctx.author.id] = await ctx.reply(
                    content=f"{ctx.author.mention} :warning: Your run job has completed with return code 1.\n\n```\n{output}\n```"
                )
                return

            if output.raw_json["run"]["stdout"] == "":
                self.RUN_CACHE[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :warning: Your run job has completed with return code 0.\n\n```\n[No output]\n```"
                )
                return

            else:
                self.RUN_CACHE[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :white_check_mark: Your run job has completed with return code 0.\n\n```\n{output}\n```"
                )
                return

        except Exception:
            output = await self.pysclient.execute(str(lang), [File(matches[0][2])])

            if (
                output.raw_json["run"]["stdout"] == ""
                and output.raw_json["run"]["stderr"]
            ):
                self.RUN_CACHE[ctx.author.id] = await ctx.reply(
                    content=f"{ctx.author.mention} :warning: Your run job has completed with return code 1.\n\n```\n{output}\n```"
                )
                return

            if output.raw_json["run"]["stdout"] == "":
                self.RUN_CACHE[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :warning: Your run job has completed with return code 0.\n\n```\n[No output]\n```"
                )
                return

            else:
                self.RUN_CACHE[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :white_check_mark: Your run job has completed with return code 0.\n\n```\n{output}\n```"
                )
                return

    @commands.command(name="run", aliases=["runl"])
    async def run(self, ctx: commands.Context, lang, *, code: str):
        """Runs code."""
        async with ctx.typing():
            await self.run_code(ctx, lang, code)

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        prefix = await self.bot.command_prefix(self.bot, after)
        cmd = self.bot.get_command(after.content.lower().replace(prefix, ""))
        try:
            if after.content.lower().startswith(f"{prefix}run"):
                await after.add_reaction("🔁")

            def check(reaction, user):
                return user == after.author and str(reaction.emoji) == "🔁"

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=30, check=check
                )
            except asyncio.TimeoutError:
                await after.clear_reaction("🔁")
            else:
                msg: disnake.Message = self.RUN_CACHE[after.author.id]

                if msg:
                    await msg.delete()

                ctx = await self.bot.get_context(after)
                await cmd.invoke(ctx)
                await after.clear_reaction("🔁")

        except Exception:
            return

    @commands.command()
    async def echo(
        self,
        ctx: commands.Context,
        channel: Optional[disnake.abc.GuildChannel],
        member: disnake.User,
        *,
        message: Union[str, int],
    ):
        """
        Echo's a message using a webhook.
        """

        channel = channel or ctx.channel

        await ctx.message.delete()
        avatar = await member.display_avatar.with_static_format("png").read()
        webhook = await channel.create_webhook(name=member.name, avatar=avatar)
        await webhook.send(message)
        await webhook.delete()

    @commands.command(name="say", description="Says whatever you want for you.")
    async def say(self, ctx: commands.Context, *, text: str):
        await ctx.send(text)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mlb(self, ctx):
        """The global message leaderboard."""

        db = await self.msg.find().sort("messages", -1).to_list(100000)

        view = utils.MyPages(db)
        await view.start(ctx, per_page=10)

    @commands.Cog.listener("on_message")
    async def message_increment(self, message: disnake.Message):

        if message.author.bot:
            return

        if str(message.channel.type) != "text":
            return

        db = self.bot.mongo["discord"]["messages"]

        data = await db.find_one({"_id": message.author.id})

        if data is None:
            await db.insert_one(
                {"_id": message.author.id, "messages": 1, "name": str(message.author)}
            )

        if data is not None:
            await db.update_one({"_id": message.author.id}, {"$inc": {"messages": 1}})
            await db.update_one(
                {"_id": message.author.id}, {"$set": {"name": str(message.author)}}
            )

    @commands.Cog.listener("on_message")
    async def github_link(self, message: disnake.Message):
        if str(message.channel.type) != "text":
            return
        if message.guild.id != 926115595307614249:
            return

        for text in message.content.split():
            if text.startswith("##"):
                await message.channel.send(
                    f"https://github.com/CaedenPH/Jarvide/pull/{text.replace('##', '')}"
                )
                return

    @commands.command(hidden=True)
    async def translate(self, ctx, *, message: commands.clean_content = None):
        """Translates a message to English using Google translate."""

        loop = self.bot.loop
        if message is None:
            ref = ctx.message.reference
            if ref and isinstance(ref.resolved, disnake.Message):
                message = ref.resolved.content
            else:
                return await ctx.send("Missing a message to translate.")

        try:
            ret = await loop.run_in_executor(None, self.trans.translate, message)
        except Exception as e:
            return await ctx.send(f"An error occurred: {e.__class__.__name__}: {e}")

        embed = disnake.Embed(title="Translated", colour=0x4284F3)
        src = googletrans.LANGUAGES.get(ret.src, "(auto-detected)").title()
        dest = googletrans.LANGUAGES.get(ret.dest, "Unknown").title()
        embed.add_field(name=f"From {src}", value=ret.origin, inline=False)
        embed.add_field(name=f"To {dest}", value=ret.text, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Helpful(bot))
