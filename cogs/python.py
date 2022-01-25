from disnake.ext import commands
from utils.rtfm import fuzzy
from typing import Dict
import re
import os
import disnake
from datetime import datetime
import random
from utils.replies import REPLIES
from utils.classes import DeleteView, SphinxObjectFileReader
from io import StringIO


class Python(commands.Cog):
    """Commands relating to the python langage."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:python:930713365758771242>"
        self.pypi_db = self.bot.mongo["discord"]["pypi"]
        self.docs_cache = []
        self.cache_items_for_docs()

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
        name="docs", aliases=["rtfd", "rtfm", "d", "doc"], invoke_without_command=True
    )
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

    @commands.slash_command()
    async def docs(self, inter, object: str):

        data = getattr(disnake, object.replace("disnake.", ""))
        file = StringIO()
        file.write(data.__doc__)
        file.seek(0)
        await inter.response.send_message(file=disnake.File(file, filename="file.txt"))

    @docs.autocomplete(option_name="object")
    async def docs_autocomplete(
        self, inter: disnake.ApplicationCommandInteraction, object: str
    ) -> str:

        return [obj for obj in self.docs_cache if obj.lower() in object.lower()]

    def cache_items(self, *inventories):

        for inventory in inventories:
            for obj in dir(inventory):
                if obj not in self.docs_cache:
                    self.docs_cache.append(f"disnake.{obj}")

    def cache_items_for_docs(self):
        self.cache_items(
            disnake,
        )


def setup(bot):
    bot.add_cog(Python(bot))