import asyncio
import re

import discord
import googletrans
from discord.ext import commands
from pyston import File, PystonClient

from utils.paginator import Paginator

CODE_REGEX = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")


class MyPages:

    __slots__ = ("data")

    def __init__(self, data: list):
        self.data = data

    async def start(self, ctx: commands.Context, *, per_page: int):
        embeds = []

        for i in range(0, len(self.data), per_page):
            embed = discord.Embed(
                title="Global Message Leaderboard",
                description="",
            )
            for index, user in enumerate(self.data[i : i + per_page]):
                embed.description += (
                    f"\n{index+1}. **{user['name']}**: {user['messages']: ,}"
                )

            embeds.append(embed)

        for index, embed in enumerate(embeds):
            embed.set_footer(text=f"Page {index+1}/{len(embeds)}")

        view = Paginator(ctx, embeds, embed=True)

        view.msg = await ctx.send(embed=embeds[0], view=view)


class Helpful(commands.Cog):

    """Helpful commands."""

    def __init__(self, bot):
        self.pysclient = PystonClient()
        self.bot = bot
        self._run_cache = {}
        self.translator = googletrans.Translator()

    @property
    def emoji(self) -> str:
        return "😄"

    async def run_code(self, ctx: commands.Context, lang: str, code: str) -> None:
        try:
            lang = lang.split("```")[1]
            code = code.split("```")[0]
            output = await self.pysclient.execute(str(lang), [File(code)])

            if (
                output.raw_json["run"]["stdout"] == ""
                and output.raw_json["run"]["stderr"]
            ):
                self._run_cache[ctx.author.id] = await ctx.reply(
                    content=f"{ctx.author.mention} :warning: Your {lang} job has completed with return code 1.\n\n```\n{output}\n```"
                )
                return

            if output.raw_json["run"]["stdout"] == "":
                self._run_cache[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :warning: Your {lang} job has completed with return code 0.\n\n```\n[No output]\n```"
                )
                return

            else:
                
                if len(output) >= 100:
                    output = output[:100] + "\n... (truncated, too many lines)"
                    
                self._run_cache[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :white_check_mark: Your {lang} job has completed with return code 0.\n\n```\n{output}\n```"
                )
                return

        except Exception:
            output = await self.pysclient.execute(lang, [File(code)])

            if (
                output.raw_json["run"]["stdout"] == ""
                and output.raw_json["run"]["stderr"]
            ):
                self._run_cache[ctx.author.id] = await ctx.reply(
                    content=f"{ctx.author.mention} :warning: Your {lang} job has completed with return code 1.\n\n```\n{output}\n```"
                )
                return

            if output.raw_json["run"]["stdout"] == "":
                self._run_cache[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :warning: Your {lang} job has completed with return code 0.\n\n```\n[No output]\n```"
                )
                return

            else:
                if len(output) >= 100:
                    output = output[:100] + "\n... (truncated, too many lines)"
                    
                self._run_cache[ctx.author.id] = await ctx.send(
                    content=f"{ctx.author.mention} :white_check_mark: Your {lang} job has completed with return code 0.\n\n```\n{output}\n```"
                )
                return


    @commands.command(name="run")
    async def run(self, ctx: commands.Context, lang, *, code: str):
        """Run some code."""
        async with ctx.typing():
            await self.run_code(ctx, lang, code)

    @commands.Cog.listener("on_message_edit")
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
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
                msg: discord.Message = self._run_cache[after.author.id]

                if msg:
                    await msg.delete()

                await cmd.invoke(ctx)
                await after.clear_reaction("🔁")

        except Exception:
            return

    @commands.command(name="say")
    async def say(self, ctx: commands.Context, *, text: str):
        """Says whatever you want for you :D"""
        await ctx.send(text)


    @commands.command(name="translate")
    async def translate(
        self, ctx: commands.Context, *, message: commands.clean_content = None
    ):
        """Translates a message using google translate."""

        if message is None:
            ref = ctx.message.reference
            if ref and isinstance(ref.resolved, discord.Message):
                message = ref.resolved.content
            else:
                return await ctx.send("Missing a message to translate.")

        try:
            ret = await self.bot.loop.run_in_executor(
                None, self.translator.translate, message
            )
        except Exception as e:
            return await ctx.send(f"An error occurred: {e.__class__.__name__}: {e}")

        embed = discord.Embed(title="Translated", colour=0x4284F3)
        src = googletrans.LANGUAGES.get(ret.src, "(auto-detected)").title()
        dest = googletrans.LANGUAGES.get(ret.dest, "Unknown").title()
        embed.add_field(name=f"From {src}", value=ret.origin, inline=False)
        embed.add_field(name=f"To {dest}", value=ret.text, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Helpful(bot))
