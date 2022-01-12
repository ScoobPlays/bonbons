from typing import Union, Optional, Dict
from pyston import PystonClient, File
from disnake.ext import commands
from utils.rtfm import fuzzy
from random import choice
import disnake
import utils
import re
import asyncio
import io
import os
import zlib


class SphinxObjectFileReader:
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode("utf-8")

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b""
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b"\n")
            while pos != -1:
                yield buf[:pos].decode("utf-8")
                buf = buf[pos + 1 :]
                pos = buf.find(b"\n")


class Helpful(commands.Cog, description="Commands that may be helpful."):
    def __init__(self, bot):
        self.pysclient = PystonClient()
        self.CODE_REGEX = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")
        self.bot = bot
        self.db = self.bot.mongo["discord"]["bot"]
        self.RUN_CACHE = {}
        self.msg = self.bot.mongo["discord"]["messages"]

    @property
    def emoji(self):
        return "🫂"

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        tag = await self.db.find_one({"_id": self.bot.user.id})

        if not tag:
            await self.db.insert_one({"_id": self.bot.user.id, "uses": 0})

        uses = tag["uses"] + 1

        await self.db.update_one(tag, {"$set": {"uses": int(uses)}})
        self.bot.invoked_commands = uses

    def created_at(self, value):
        return f"<t:{int(disnake.Object(value).created_at.timestamp())}:F> (<t:{int(disnake.Object(value).created_at.timestamp())}:R>)"

    async def run_code(self, ctx: commands.Context, lang, code: str):
        matches = self.CODE_REGEX.findall(code)
        code = matches[0][2]
        output = await self.pysclient.execute(str(lang), [File(code)])

        if output.raw_json["run"]["stdout"] == "" and output.raw_json["run"]["stderr"]:
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

            if lang.lower().startswith("```"):
                return await ctx.send(
                    f"```\n{ctx.command.name} {ctx.command.signature}\n```\nNot enough arguments passed."
                )

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

        try:
            await ctx.message.delete()
            avatar = await member.display_avatar.with_static_format("png").read()
            webhook = await channel.create_webhook(name=member.name, avatar=avatar)
            await webhook.send(message)
            await webhook.delete()
        except Exception as e:
            return await ctx.send(
                embed=disnake.Embed(description=e, color=disnake.Color.red())
            )

    @commands.command(name="say", help="Says whatever you want for you.")
    async def say(self, ctx: commands.Context, *, text: str):
        await ctx.send(text)

    @commands.command()
    async def pypi(self, ctx: commands.Context, name: str):
        """Finds a package on PyPI."""
        async with ctx.typing():
            async with self.bot.session.get(
                f"https://pypi.org/pypi/{name}/json"
            ) as data:
                if data.status == 200:
                    raw = await data.json()

                    embed = disnake.Embed(
                        title=name,
                        description=raw["info"]["summary"],
                        url=raw["info"]["project_url"],
                        color=disnake.Color.greyple(),
                    ).set_thumbnail(
                        url="https://cdn.discordapp.com/emojis/766274397257334814.png"
                    )
                    await ctx.send(embed=embed)

                else:
                    await ctx.send("A package with that name does not exist.")

    @commands.slash_command(name="pypi")
    async def pypi_slash(self, inter, name: str):
        """Finds a package on PyPI."""
        async with self.bot.session.get(f"https://pypi.org/pypi/{name}/json") as data:
            if data.status == 200:
                raw = await data.json()

                embed = disnake.Embed(
                    title=name,
                    description=raw["info"]["summary"],
                    url=raw["info"]["project_url"],
                    color=disnake.Color.greyple(),
                ).set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/766274397257334814.png"
                )
                await inter.response.send_message(embed=embed)

            else:
                await inter.response.send_message(
                    "A package with that name does not exist.", ephemeral=True
                )

    def parse_object_inv(self, stream: SphinxObjectFileReader, url: str) -> Dict:
        result = {}
        inv_version = stream.readline().rstrip()

        if inv_version != "# Sphinx inventory version 2":
            raise RuntimeError("Invalid objects.inv file version.")

        projname = stream.readline().rstrip()[11:]
        stream.readline().rstrip()[11:]

        line = stream.readline()
        if "zlib" not in line:
            raise RuntimeError("Invalid objects.inv file, not z-lib compatible.")

        entry_regex = re.compile(r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)")
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(":")
            if directive == "py:module" and name in result:
                continue

            if directive == "std:doc":
                subdirective = "label"

            if location.endswith("$"):
                location = location[:-1] + name

            key = name if dispname == "-" else dispname
            prefix = f"{subdirective}:" if domain == "std" else ""

            key = (
                key.replace("disnake.ext.commands.", "")
                .replace("disnake.ext.menus.", "")
                .replace("disnake.ext.ipc.", "")
                .replace("disnake.", "")
            )

            result[f"{prefix}{key}"] = os.path.join(url, location)

        return result

    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            async with self.bot.session.get(page + "/objects.inv") as resp:
                if resp.status != 200:
                    raise RuntimeError(
                        "Cannot build rtfm lookup table, try again later."
                    )

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._rtfm_cache = cache

    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            "python": "https://docs.python.org/3",
            "disnake": "https://disnake.readthedocs.io/en/latest",
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, "_rtfm_cache"):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r"^(?:disnake\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)

        if key.startswith("master"):
            q = obj.lower()
            for name in dir(disnake.abc.Messageable):
                if name[0] == "_":
                    continue
                if q == name:
                    obj = f"abc.Messageable.{name}"
                    break

        cache = list(self._rtfm_cache[key].items())

        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = disnake.Embed(colour=disnake.Colour.blurple())
        if len(matches) == 0:
            responses = (
                "I looked far and wide but nothing was found",
                "I could not find anything related to your query.",
                "Could not find anything. Sorry.",
                "I didn't find anything related to your query.",
            )
            return await ctx.send(choice(responses))

        e.description = "\n".join(f"[`{key}`]({url})" for key, url in matches)
        ref = ctx.message.reference
        refer = None
        if ref and isinstance(ref.resolved, disnake.Message):
            refer = ref.resolved.to_reference()
        await ctx.send(embed=e, reference=refer)

    @commands.group(name="rtfm", aliases=["rtfd"], invoke_without_command=True)
    async def rtfm_group(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve documentation on Python libraries."""

        await self.do_rtfm(ctx, "disnake", obj)

    @rtfm_group.command(name="python", aliases=["py"])
    async def rtfm_python_cmd(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation about the Python language."""
        await self.do_rtfm(ctx, "python", obj)

    @rtfm_group.command(name="disnake")
    async def rtfm_disnake_cmd(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation about the Disnake library."""
        await self.do_rtfm(ctx, "disnake", obj)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mlb(self, ctx):
        """Global message leaderboard."""
        # implement name changing for `name` using on_member_update

        db = await self.msg.find().sort("messages", -1).to_list(100000)

        view = utils.MyPages(db)
        await view.start(ctx, per_page=10)


def setup(bot):
    bot.add_cog(Helpful(bot))
