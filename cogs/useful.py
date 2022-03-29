import io
import os
import random
import re
import zlib
from typing import Dict
import time

import discord
from discord.ext import commands

from utils.constants import REPLIES


class SphinxObjectFileReader:
    BUFSIZE = 16 * 1024

    def __init__(self, buffer: bytes):
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


class RTFMView(discord.ui.View):
    def __init__(
        self,
        reference: discord.MessageReference,
        embed: discord.Embed,
        ctx: commands.Context,
        now: float,
        when: float,
        ):
        super().__init__()
        self.reference = reference
        self.embed = embed
        self.ctx = ctx
        self.now = now
        self.when = when

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return False
        return True

    def _update_labels(self):
        self.took_when.label = f"Took{self.now-self.when: .3f}"

    async def start(self, ctx: commands.Context):
        self._update_labels()
        await self.ctx.send(embed=self.embed, reference=self.reference, view=self)

    @discord.ui.button(emoji="🗑️")
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()

        await interaction.delete_original_message()

    @discord.ui.button(label=f"...", disabled=True)
    async def took_when(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


class Useful(commands.Cog, description="Commands that I think are useful to me."):
    def __init__(self, bot):
        self.bot = bot

    @property
    def emoji(self) -> str:
        return "🗯️"

    @staticmethod
    async def send_error_message(
        ctx: commands.Context, message: discord.Message
    ) -> None:
        embed = discord.Embed(
            title=random.choice(REPLIES),
            description=message,
            color=discord.Color.red(),
        )
        return await ctx.send(embed=embed)

    @staticmethod
    def finder(text, collection, *, key=None, lazy=True) -> list:
        suggestions = []
        text = str(text)
        pat = ".*?".join(map(re.escape, text))
        regex = re.compile(pat, flags=re.IGNORECASE)

        for item in collection:
            to_search = key(item) if key else item
            r = regex.search(to_search)
            if r:
                suggestions.append((len(r.group()), r.start(), item))

        def sort_key(tup):
            if key:
                return tup[0], tup[1], key(tup[2])
            return tup

        if lazy:
            return (z for _, _, z in sorted(suggestions, key=sort_key))
        else:
            return [z for _, _, z in sorted(suggestions, key=sort_key)]

    @staticmethod
    def parse_object_inv(stream: SphinxObjectFileReader, url: str) -> Dict:
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
                key.replace("discord.ext.commands.", "")
                .replace("discord.ext.menus.", "")
                .replace("discord.ext.ipc.", "")
                .replace("discord.", "")
            )

            result[f"{prefix}{key}"] = os.path.join(url, location)

        return result

    async def build_rtfm_lookup_table(self, page_types: dict):
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

    async def do_rtfm(self, ctx: commands.Context, key: str, obj: str):
        now = time.perf_counter()

        page_types = {
            "python": "https://docs.python.org/3",
            "discord": "https://discord.readthedocs.io/en/latest",
            "nextcord": "https://nextcord.readthedocs.io/en/latest",
            "discord.py": "https://discordpy.readthedocs.io/en/master",
            "pycord": "https://docs.pycord.dev/en/master/",
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, "_rtfm_cache"):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r"^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)

        if key.startswith("master"):
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == "_":
                    continue
                if q == name:
                    obj = f"abc.Messageable.{name}"
                    break

        cache = list(self._rtfm_cache[key].items())

        matches = self.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        embed = discord.Embed(colour=0x2F3136)
        if len(matches) == 0:
            responses = (
                "I looked far and wide but nothing was found.",
                "I could not find anything related to your query.",
                "Could not find anything. Sorry.",
                "I didn't find anything related to your query.",
            )
            return await self.send_error_message(ctx, random.choice(responses))

        embed.description = "\n".join(f"[`{key}`]({url})" for key, url in matches)
        ref = ctx.message.reference
        reference = None
        if ref and isinstance(ref.resolved, discord.Message):
            reference = ref.resolved.to_reference()

        done = time.perf_counter()
        view = RTFMView(reference=reference, embed=embed, ctx=ctx, now=done, when=now)
        view._update_labels()
        await view.start(ctx)

    @commands.group(
        name="rtfm",
        aliases=("rtfd", "docs", "d", "doc"),
        invoke_without_command=True,
        case_insensitive=True,
    )
    async def rtfm_group(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve documentation on python libraries."""

        await self.do_rtfm(ctx, "discord.py", obj)

    @rtfm_group.command(name="python", aliases=("py",))
    async def rtfm_python_cmd(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation on the python language."""
        await self.do_rtfm(ctx, "python", obj)

    @rtfm_group.command(name="nextcord", aliases=("nc",))
    async def rtfm_nextcord(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation on nextcord"""
        await self.do_rtfm(ctx, "nextcord", obj)

    @rtfm_group.command(name="discord")
    async def rtfm_discord(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation on discord.py."""
        await self.do_rtfm(ctx, "discord", obj)

    @rtfm_group.command(name="pycord", aliases=("pyc",))
    async def rtfm_discord(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation on pycord."""
        await self.do_rtfm(ctx, "pycord", obj)
        
    @commands.command(name="pypi")
    async def pypi(self, ctx: commands.Context, name: str):

        """Finds a package on PyPI."""

        async with ctx.typing():
            async with self.bot.session.get(
                f"https://pypi.org/pypi/{name}/json"
            ) as data:
                if data.status == 200:
                    raw = await data.json()

                    embed = discord.Embed(
                        title=raw["info"]["name"],
                        description=raw["info"]["summary"],
                        url=raw["info"]["project_url"],
                        color=discord.Color.greyple(),
                    ).set_thumbnail(
                        url="https://cdn.discordapp.com/emojis/766274397257334814.png"
                    )
                    await ctx.send(embed=embed)

                else:
                    await ctx.reply("A package with that name does not exist!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Useful(bot))
