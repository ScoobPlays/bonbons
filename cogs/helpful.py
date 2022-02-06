import asyncio
import re
from typing import Optional, Union

import disnake
import googletrans
from disnake.ext import commands
from pyston import File, PystonClient

from utils.paginators import MyPages

CODE_REGEX = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")


class Helpful(commands.Cog):
    """Commands that may be helpful?"""

    def __init__(self, bot):
        self.pysclient = PystonClient()
        self.bot = bot
        self.emoji = "🫂"
        self.bot_database = self.bot.mongo["discord"]["bot"]
        self._run_cache = {}
        self.message_database = self.bot.mongo["discord"]["messages"]
        self.translator = googletrans.Translator()

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        tag = await self.bot_database.find_one({"_id": self.bot.user.id})

        await self.bot_database.update_one(tag, {"$inc": {"uses": 1}})

        self.bot.invoked_commands = tag["uses"] + 1

    async def run_code(self, ctx: commands.Context, lang: str, code: str) -> None:
        matches = CODE_REGEX.findall(code)

        try:
            lang = lang.split("```")[1]
            code = code.split("```")[0]
            output = await self.pysclient.execute(str(lang), [File(code)])

            if (
                output.raw_json["run"]["stdout"] == ""
                and output.raw_json["run"]["stderr"]
            ):
                self._run_cache[ctx.author.id] = await ctx.reply(
                    content=f"{ctx.author.mention} :warning: Your run job has completed with return code 1.\n\n```\n{output}\n```"
                )
                return

            if output.raw_json["run"]["stdout"] == "":
                self._run_cache[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :warning: Your run job has completed with return code 0.\n\n```\n[No output]\n```"
                )
                return

            else:
                self._run_cache[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :white_check_mark: Your run job has completed with return code 0.\n\n```\n{output}\n```"
                )
                return

        except Exception:
            print(lang, code)
            output = await self.pysclient.execute(lang, [File(code)])

            if (
                output.raw_json["run"]["stdout"] == ""
                and output.raw_json["run"]["stderr"]
            ):
                self._run_cache[ctx.author.id] = await ctx.reply(
                    content=f"{ctx.author.mention} :warning: Your run job has completed with return code 1.\n\n```\n{output}\n```"
                )
                return

            if output.raw_json["run"]["stdout"] == "":
                self._run_cache[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :warning: Your run job has completed with return code 0.\n\n```\n[No output]\n```"
                )
                return

            else:
                self._run_cache[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :white_check_mark: Your run job has completed with return code 0.\n\n```\n{output}\n```"
                )
                return

    async def _run_code(self, inter, code: str):
        matches = CODE_REGEX.findall(str(code))
        print(matches)
        print(code)
        language = matches[0][1]
        code = matches[0][2]

        output = await self.pysclient.execute(str(language), [File(code)])

        if output.raw_json["run"]["stdout"] == "" and output.raw_json["run"]["stderr"]:
            return await inter.response.send_message(
                content=f"{inter.author.mention} :warning: Your run job has completed with return code 1.\n\n```\n{output}\n```"
            )

        if output.raw_json["run"]["stdout"] == "":
            return await inter.response.send_message(
                content=f"{inter.author.mention} :warning: Your run job has completed with return code 0.\n\n```\n[No output]\n```"
            )

        else:
            return await inter.response.send_message(
                content=f"{inter.author.mention} :white_check_mark: Your run job has completed with return code 0.\n\n```\n{output}\n```"
            )

    @commands.command(name="run", aliases=["runl"])
    async def run(self, ctx: commands.Context, lang, *, code: str):
        """Runs code."""
        async with ctx.typing():
            await self.run_code(ctx, lang, code)

    @commands.message_command(name="Run Code")
    async def run(self, inter, message: disnake.Message):
        await self._run_code(inter, message.content.replace(".run", ""))

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        ctx = await self.bot.get_context(after)
        cmd = self.bot.get_command(after.content.lower().replace(str(ctx.prefix), ""))
        try:
            if after.content.lower().startswith(f"{ctx.prefix}run"):
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
                msg: disnake.Message = self._run_cache[after.author.id]

                if msg:
                    await msg.delete()

                await cmd.invoke(ctx)
                await after.clear_reaction("🔁")

        except Exception:
            return

    @commands.command()  # TODO: Optimize this.
    @commands.is_owner()
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

    @commands.command(name="say")
    async def say(self, ctx: commands.Context, *, text: str):
        """Says whatever you want for you."""
        await ctx.send(text)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mlb(self, ctx):
        """The global message leaderboard."""

        db = await self.message_database.find().sort("messages", -1).to_list(100000)

        view = MyPages(db)
        await view.start(ctx, per_page=10)

    @commands.Cog.listener("on_message")
    async def message_increment(self, message: disnake.Message):

        if message.author.bot:
            return

        data = await self.message_database.find_one({"_id": message.author.id})

        if data is None:
            await self.message_database.insert_one(
                {"_id": message.author.id, "messages": 1, "name": str(message.author)}
            )

        if data is not None:
            await self.message_database.update_one(
                {"_id": message.author.id}, {"$inc": {"messages": 1}}
            )
            await self.message_database.update_one(
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
    async def translate(
        self, ctx: commands.Context, *, message: commands.clean_content = None
    ):
        """Translates a message to using google translate."""

        if message is None:
            ref = ctx.message.reference
            if ref and isinstance(ref.resolved, disnake.Message):
                message = ref.resolved.content
            else:
                return await ctx.send("Missing a message to translate.")

        try:
            ret = await self.bot.loop.run_in_executor(
                None, self.translator.translate, message
            )
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
