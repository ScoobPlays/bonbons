import disnake
from disnake.ext import commands
import json
from datetime import datetime
import base64
import random
import aiohttp
from contextlib import suppress
from utils.funcs import b64_encode, b64_decode, Google


class Extra(commands.Cog, description="Extra commands."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="google")
    async def google(self, ctx: commands.Context, *, query: str):

        """Returns a google link for a query."""

        await ctx.send(f"Google Result for: `{query}`", view=Google(query))

    @commands.slash_command(name="google")
    async def google_slash(
        self, inter: disnake.ApplicationCommandInteraction, query: str
    ):
        """Returns a google link for a query"""

        await inter.response.send_message(
            f"Google Result for: `{query}`", view=Google(query), ephemeral=False
        )

    @commands.command(name="say", help="Says whatever you want for you.")
    async def say(self, ctx: commands.Context, *, argument: str):
        await ctx.send(argument)

    @commands.slash_command(name="say")
    async def say_slash(
        self, inter: disnake.ApplicationCommandInteraction, argument: str
    ):
        "Says whatever you want for you"
        await inter.response.send_message(argument, ephemeral=False)

    @commands.slash_command()
    async def base64(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @base64.sub_command()
    async def encode(self, inter: disnake.ApplicationCommandInteraction, argument: str):
        """Encodes a message into a base64 string"""
        try:
            await inter.response.send_message(
                await b64_encode(argument), ephemeral=False
            )
        except Exception:
            await inter.response.send_message(
                f"Couldn't encode that message.", ephemeral=False
            )

    @base64.sub_command()
    async def decode(self, inter: disnake.ApplicationCommandInteraction, argument: str):
        """Decodes a base64 string"""
        try:
            await inter.response.send_message(
                await b64_decode(argument), ephemeral=False
            )
        except Exception:
            await inter.response.send_message(
                "Couldn't decode that message.", ephemeral=False
            )

    @commands.command(name="wikipedia", aliases=("wiki",))
    async def wikipedia_cmd(self, ctx: commands.Context, *, query: str):
        """Searches for something on the wikipedia"""
        async with self.bot.session.get(
            (
                "https://en.wikipedia.org//w/api.php?action=query"
                "&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop="
            ).format(query)
        ) as r:
            sea = (await r.json())["query"]

            if sea["searchinfo"]["totalhits"] == 0:
                await ctx.send("Sorry, your search could not be found.")
            else:
                for x in range(len(sea["search"])):
                    article = sea["search"][x]["title"]
                    async with self.bot.session.get(
                        "https://en.wikipedia.org//w/api.php?action=query"
                        "&utf8=1&redirects&format=json&prop=info|images"
                        "&inprop=url&titles={}".format(article)
                    ) as r:
                        req = (await r.json())["query"]["pages"]
                        if str(list(req)[0]) != "-1":
                            break
                else:
                    await ctx.send("Sorry, your search could not be found.")
                    return
                article = req[list(req)[0]]["title"]
                arturl = req[list(req)[0]]["fullurl"]
                async with self.bot.session.get(
                    "https://en.wikipedia.org/api/rest_v1/page/summary/" + article
                ) as r:
                    artdesc = (await r.json())["extract"]
                embed = disnake.Embed(
                    title="**" + article + "**",
                    url=arturl,
                    description=artdesc,
                    color=0x3FCAFF,
                )
                embed.set_footer(
                    text=f"Search result for {query}",
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png",
                )
                embed.set_author(
                    name="Wikipedia",
                    url="https://en.wikipedia.org/",
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png",
                )
                embed.timestamp = datetime.utcnow()
                await ctx.send(embed=embed)

    @commands.slash_command(name="wikipedia", aliases=("wiki",))
    async def wikipedia_slash(self, inter, query: str):
        """Searches for something on the wikipedia"""
        async with self.bot.session.get(
            (
                "https://en.wikipedia.org//w/api.php?action=query"
                "&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop="
            ).format(query)
        ) as r:
            sea = (await r.json())["query"]

            if sea["searchinfo"]["totalhits"] == 0:
                await inter.response.send_message(
                    "Sorry, your search could not be found.", ephemeral=False
                )
            else:
                for x in range(len(sea["search"])):
                    article = sea["search"][x]["title"]
                    async with self.bot.session.get(
                        "https://en.wikipedia.org//w/api.php?action=query"
                        "&utf8=1&redirects&format=json&prop=info|images"
                        "&inprop=url&titles={}".format(article)
                    ) as r:
                        req = (await r.json())["query"]["pages"]
                        if str(list(req)[0]) != "-1":
                            break
                else:
                    return await inter.response.send_message(
                        "Sorry, your search could not be found.", ephemeral=False
                    )
                article = req[list(req)[0]]["title"]
                arturl = req[list(req)[0]]["fullurl"]
                async with self.bot.session.get(
                    "https://en.wikipedia.org/api/rest_v1/page/summary/" + article
                ) as r:
                    artdesc = (await r.json())["extract"]
                embed = disnake.Embed(
                    title="**" + article + "**",
                    url=arturl,
                    description=artdesc,
                    color=0x3FCAFF,
                )
                embed.set_footer(
                    text=f"Search result for {query}",
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png",
                )
                embed.set_author(
                    name="Wikipedia",
                    url="https://en.wikipedia.org/",
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png",
                )
                embed.timestamp = datetime.utcnow()
                await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(
        name="minecraft",
        aliases=(
            "skin",
            "mc",
        ),
    )
    async def minecraft_cmd(self, ctx: commands.Context, username="Notch"):
        """Fetches information about a minecraft user."""

        async with self.bot.session.get(
            "https://api.mojang.com/users/profiles/minecraft/{}".format(username)
        ) as r:
            uuid = (await r.json())["id"]

        async with self.bot.session.get(
            "https://sessionserver.mojang.com/session/minecraft/profile/{}".format(uuid)
        ) as r:
            value = (await r.json())["properties"][0]["value"]
        url = json.loads(base64.b64decode(value).decode("utf-8"))["textures"]["SKIN"][
            "url"
        ]

        async with self.bot.session.get(
            "https://api.mojang.com/user/profiles/{}/names".format(uuid)
        ) as r:
            names = await r.json()
        history = ""
        for name in reversed(names):
            history += name["name"] + "\n"

        embed = disnake.Embed(title=f"User Information For {username}")
        embed.add_field(name="Username", value=username)
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.add_field(name="History", value=history)
        embed.set_thumbnail(url=url)
        embed.set_footer(icon_url=ctx.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.slash_command(
        name="minecraft",
    )
    async def minecraft_slash(
        self, inter: disnake.ApplicationCommandInteraction, username="Notch"
    ):
        """Fetches information about a minecraft user"""

        async with self.bot.session.get(
            "https://api.mojang.com/users/profiles/minecraft/{}".format(username)
        ) as r:
            uuid = (await r.json())["id"]

        async with self.bot.session.get(
            "https://sessionserver.mojang.com/session/minecraft/profile/{}".format(uuid)
        ) as r:
            value = (await r.json())["properties"][0]["value"]
        url = json.loads(base64.b64decode(value).decode("utf-8"))["textures"]["SKIN"][
            "url"
        ]

        async with self.bot.session.get(
            "https://api.mojang.com/user/profiles/{}/names".format(uuid)
        ) as r:
            names = await r.json()
        history = ""
        for name in reversed(names):
            history += name["name"] + "\n"

        embed = disnake.Embed(title=f"User Information For {username}")
        embed.add_field(name="Username", value=username)
        embed.set_author(name=inter.author, icon_url=inter.author.display_avatar)
        embed.add_field(name="History", value=history)
        embed.set_thumbnail(url=url)
        embed.set_footer(icon_url=inter.author.display_avatar)
        embed.timestamp = datetime.utcnow()
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="kiss", help="Kisses a user.")
    @commands.guild_only()
    async def kiss_cmd(self, ctx: commands.Context, member: disnake.Member):
        await ctx.send(
            f"{ctx.author.mention} kissed {member.mention}!!\nhttps://tenor.com/view/milk-and-mocha-bear-couple-kisses-kiss-love-gif-12498627"
        )

    @commands.slash_command(name="kiss")
    @commands.guild_only()
    async def kiss_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Kisses a user"""
        await inter.response.send_message(
            f"{inter.author.mention} kissed {member.mention}!!\nhttps://tenor.com/view/milk-and-mocha-bear-couple-kisses-kiss-love-gif-12498627",
            ephemeral=False,
        )

    @commands.command(name="bonk", help="Bonks a user.")
    @commands.guild_only()
    async def bonk_cmd(self, ctx: commands.Context, member: disnake.Member):
        bonkis = [
            "https://tenor.com/view/despicable-me-minions-bonk-hitting-cute-gif-17663380",
            "https://tenor.com/view/lol-gif-21667170",
            "https://tenor.com/view/azura-bonk-azura-bonk-gif-21733152",
        ]
        bonkiuwu = random.choice(bonkis)
        await ctx.send(f"{ctx.author.mention} bonked {member.mention}!\n{bonkiuwu}")

    @commands.slash_command(name="bonk", help="Bonks a user")
    @commands.guild_only()
    async def bonk_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Bonks a user"""
        bonkis = [
            "https://tenor.com/view/despicable-me-minions-bonk-hitting-cute-gif-17663380",
            "https://tenor.com/view/lol-gif-21667170",
            "https://tenor.com/view/azura-bonk-azura-bonk-gif-21733152",
        ]
        bonkiuwu = random.choice(bonkis)
        await inter.response.send_message(
            f"{inter.author.mention} bonked {member.mention}!\n{bonkiuwu}",
            ephemeral=False,
        )

    @commands.command(name="spank", help="Spanks a user.")
    @commands.guild_only()
    async def spank_cmd(self, ctx: commands.Context, member: disnake.Member):
        await ctx.send(
            f"{ctx.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590"
        )

    @commands.slash_command(name="spank", help="Spanks a user")
    @commands.guild_only()
    async def spank_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Spanks a user"""
        await inter.response.send_message(
            f"{inter.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590",
            ephemeral=False,
        )

    @commands.command(name="slap", help="Slaps a user.")
    @commands.guild_only()
    async def slap_cmd(self, ctx: commands.Context, member: disnake.Member):
        await ctx.send(
            f"{ctx.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299"
        )

    @commands.slash_command(name="slap")
    @commands.guild_only()
    async def slap_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Slaps a user"""
        await inter.response.send_message(
            f"{inter.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299",
            ephemeral=False,
        )

    @commands.command(name="pat", help="Pats a user.")
    @commands.guild_only()
    async def pat_cmd(self, ctx: commands.Context, member: disnake.Member):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                data = await r.json()
                image = data["link"]
                await ctx.send(
                    f"{ctx.author.mention} patted {member.mention}!!\n{image}"
                )

    @commands.slash_command(name="pat")
    @commands.guild_only()
    async def pat_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Pats a user"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                data = await r.json()
                image = data["link"]
                await inter.response.send_message(
                    f"{inter.author.mention} patted {member.mention}!!\n{image}",
                    ephemeral=False,
                )

    @commands.command(name="hug", help="Hugs a user.")
    @commands.guild_only()
    async def hug_cmd(self, ctx: commands.Context, member: disnake.Member):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                data = await r.json()
                image = data["link"]
                await ctx.send(
                    f"{ctx.author.mention} hugged {member.mention}!!\n{image}"
                )

    @commands.slash_command(name="hug")
    @commands.guild_only()
    async def hug_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Hugs a user"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                data = await r.json()
                image = data["link"]
                await inter.response.send_message(
                    f"{inter.author.mention} hugged {member.mention}!!\n{image}"
                )

    @commands.slash_command(
        name="afk"
    )  # taken directly from https://github.com/Dorukyum/Pycord-Manager
    async def afk_slash(
        self, inter: disnake.ApplicationCommandInteraction, message=None
    ):
        """Become AFK."""
        if not message:
            await inter.response.send_message("You are now AFK.")
            self.bot.cache["afk"][inter.author.id] = message
            return
        await inter.response.send_message(f"Set your AFK: {message}")
        self.bot.cache["afk"][inter.author.id] = message

        with suppress(disnake.Forbidden):
            await inter.author.edit(nick=f"[AFK] {inter.author.display_name}")

    @commands.command()  # taken directly from https://github.com/Dorukyum/Pycord-Manager
    async def afk(self, ctx: commands.Context, argument: str = None):

        """Become AFK."""

        if not argument:
            await ctx.send("You are now AFK.")
            self.bot.cache["afk"][ctx.author.id] = argument
            return
        await ctx.send(f"Set your AFK: {argument}")
        self.bot.cache["afk"][ctx.author.id] = argument

        with suppress(disnake.Forbidden):
            await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")


def setup(bot):
    bot.add_cog(Extra(bot))
