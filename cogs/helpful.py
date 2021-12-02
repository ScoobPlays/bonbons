from .utilities.utilsforanything import facepalms
import re, random, asyncio, io, os, zlib
from typing import Union, Optional, Dict
from pyston import PystonClient, File
from disnake.ext import commands
from utils.rtfm import fuzzy
from random import choice
import disnake


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


class Helpful(commands.Cog, description="Helpful utilities for the bot."):
    def __init__(self, bot):
        self.pysclient = PystonClient()
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")
        self.bot = bot
        self.last = None
        self.facepalms = random.choice(facepalms)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        ...

    def created_at(self, value) -> int:
        return f"<t:{int(disnake.Object(value).created_at.timestamp())}:F> (<t:{int(disnake.Object(value).created_at.timestamp())}:R>)"

    async def run_code(self, ctx: commands.Context, code: str):
        matches = self.regex.findall(code)
        code = matches[0][2]
        lang = matches[0][0] or matches[0][1]

        if not lang:
            return await ctx.reply(
                embed=disnake.Embed(
                    description="No language was hinted.", color=disnake.Color.red()
                )
            )
        output = await self.pysclient.execute(str(lang), [File(code)])

        msg = await ctx.reply(
            embed=disnake.Embed(description=output, color=disnake.Color.greyple())
        )
        self.last = msg

    async def on_run_code(
        self,
        before: disnake.Message,
        after: disnake.Message,
    ):
        try:
            await after.clear_reactions()
            await self.last.delete()

            if after.content.startswith(".run"):
                after = after.content.split(".run")

            matches = self.regex.findall("".join(after[1]))
            code = matches[0][2]
            lang = matches[0][0] or matches[0][1]

            if not lang:
                return await before.reply(
                    embed=disnake.Embed(
                        description="No language was hinted.", color=disnake.Color.red()
                    )
                )
            output = await self.pysclient.execute(str(lang), [File(code)])

            await before.reply(
                embed=disnake.Embed(description=output, color=disnake.Color.greyple())
            )
        except Exception:
            return

    @commands.command()
    async def run(self, ctx: commands.Context, *, code: str):
        """Runs code, must be typehinted with a language and in a codeblock."""
        await self.run_code(ctx, code)

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        try:
            if before.content.startswith(".run") and after.content.startswith(".run"):
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
                await self.on_run_code(before, after)
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
        Echo's a message.

        .echo <user> <message>

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
    async def say(self, ctx: commands.Context, argument: str):
        await ctx.send(argument)

    @commands.command()
    async def stfu(self, ctx: commands.Context):
        """
        Shut the fuck up (STFU) a message.

        .stfu `<reply to the message>`
        """
        try:
            await ctx.message.delete()
            if not ctx.message.reference:
                return await ctx.reply(f"Reply to a message first duh {self.facepalms}")
            msg = await ctx.fetch_message(ctx.message.reference.message_id)
            await msg.delete()
            await ctx.message.add_reaction("✅")
        except Exception:
            return

    @commands.command()
    async def pypi(self, ctx: commands.Context, name: str):
        """Finds a package on the Python Package Index."""
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

    @commands.command()
    async def uptime(self, ctx):
        embed = disnake.Embed(
            title="My Uptime",
            description=f"I have been online since <t:{int(self.bot.uptime)}:R>",
            color=disnake.Color.greyple(),
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
        """
        Retrieve documentation on Python libraries.

        If no argument's were passed then `disnake` will be the documentation to lookup."""
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
    async def info(self, ctx):
        """Returns the bots info."""
        ...

def setup(bot):
    bot.add_cog(Helpful(bot))
