import os
import random
import re
from datetime import datetime
from typing import Dict

import disnake
from disnake.ext import commands

from utils.classes import DeleteView, SphinxObjectFileReader
from utils.replies import REPLIES
from utils.rtfm import fuzzy


class Python(commands.Cog):
    """Commands relating to the python langage."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:python:930713365758771242>"
        self.pypi_db = self.bot.mongo["discord"]["pypi"]

    async def send_error_message(self, ctx, msg):
        embed = disnake.Embed(
            title=random.choice(REPLIES),
            description=msg,
            color=disnake.Color.red(),
        )
        await ctx.send(embed=embed)

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
        import time

        now = time.perf_counter()

        page_types = {
            "python": "https://docs.python.org/3",
            "disnake": "https://disnake.readthedocs.io/en/latest",
            "nextcord": "https://nextcord.readthedocs.io/en/latest",
            "discord.py": "https://discordpy.readthedocs.io/en/master",
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
                "I looked far and wide but nothing was found.",
                "I could not find anything related to your query.",
                "Could not find anything. Sorry.",
                "I didn't find anything related to your query.",
            )
            return await self.send_error_message(ctx, random.choice(responses))

        e.description = "\n".join(f"[`{key}`]({url})" for key, url in matches)
        ref = ctx.message.reference
        refer = None
        if ref and isinstance(ref.resolved, disnake.Message):
            refer = ref.resolved.to_reference()
        done = time.perf_counter()
        view = DeleteView(refer=refer, embed=e, ctx=ctx, now=done, when=now)
        view._update_labels()
        await view.start(ctx)

    @commands.group(
        name="rtfm",
        aliases=["rtfd"],
        invoke_without_command=True,
        case_insensitive=True,
    )
    async def rtfm_group(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve documentation on python libraries. Defaults to `discord.py` if no sub-command was passed."""

        await self.do_rtfm(ctx, "discord.py", obj)

    @rtfm_group.command(name="python", aliases=["py"])
    async def rtfm_python_cmd(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation about the python language."""
        await self.do_rtfm(ctx, "python", obj)

    @rtfm_group.command(name="nextcord", aliases=["nc"])
    async def rtfm_nextcord(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation about the nextcord library."""
        await self.do_rtfm(ctx, "nextcord", obj)

    @rtfm_group.command(name="disnake")
    async def rtfm_disnake(self, ctx: commands.Context, *, obj: str = None):
        """Retrieve's documentation about the disnake library."""
        await self.do_rtfm(ctx, "disnake", obj)

    async def insert_into_db(self, obj):
        data = await self.pypi_db.find_one({"name": obj})

        if data is None:
            await self.pypi_db.insert_one(
                {"name": obj, "inserted_at": int(datetime.now().timestamp())}
            )

        if data is not None:
            pass

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
                    await self.insert_into_db(name)

                else:
                    await ctx.send("A package with that name does not exist.")

    @commands.slash_command(name="pypi")
    async def pypi_slash(
        self, inter: disnake.ApplicationCommandInteraction, package: str
    ):
        """Finds a package on PyPI."""
        async with self.bot.session.get(
            f"https://pypi.org/pypi/{package}/json"
        ) as data:
            if data.status == 200:
                raw = await data.json()

                embed = disnake.Embed(
                    title=package,
                    description=raw["info"]["summary"],
                    url=raw["info"]["project_url"],
                    color=disnake.Color.greyple(),
                ).set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/766274397257334814.png"
                )
                await inter.response.send_message(embed=embed)
                await self.insert_into_db(package)

            else:
                await inter.response.send_message(
                    "A package with that name does not exist.", ephemeral=True
                )

    @pypi_slash.autocomplete(option_name="package")
    async def pypi_slash_autocomp(
        self, inter: disnake.ApplicationCommandInteraction, package: str
    ) -> str:
        packages = []

        for pkg in await self.pypi_db.find({}).to_list(1000):
            packages.append(pkg["name"])

        return [pkg for pkg in packages if package.lower() in pkg.lower()]


def setup(bot):
    bot.add_cog(Python(bot))
