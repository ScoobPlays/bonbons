import utils
from disnake.ext import commands
from datetime import datetime
from typing import Optional
import os
import disnake
import json
import base64
import random
import aiohttp


class General(commands.Cog, description="General commands."):
    def __init__(self, bot):
        self.bot = bot
        self.snipe_cache = None
        self.before = None
        self.emoji = '🙌'
        self.afk = self.bot.mongo["discord"]["afk"]

    def b64_encode(self, text: str):
        message_bytes = text.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        message = base64_bytes.decode("ascii")
        return message

    def b64_decode(self, text: str):
        b64msg = text.encode("ascii")
        message_bytes = base64.b64decode(b64msg)
        message = message_bytes.decode("ascii")
        return message

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):

        if message.author.bot:
            return

        self.snipe_cache = message

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):

        if before.author.bot or after.author.bot:
            return

        self.before = before

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if not isinstance(message.channel, disnake.TextChannel):
            return

        if message.author.bot:
            return

        afk_db = self.afk[str(message.guild.id)]

        data = await afk_db.find_one({"_id": message.author.id})

        if data:
            await message.channel.send(
                embed=disnake.Embed(
                    description=f"Welcome back {message.author.mention}!",
                    color=message.author.top_role.color,
                )
            )
            await afk_db.delete_one({"_id": message.author.id})

        if message.mentions:
            for member in message.mentions:
                mention_data = await afk_db.find_one({"_id": member.id})
                if mention_data:
                    if mention_data["message"] == message.id:
                        return
                    if member.id == mention_data["_id"]:
                        timestamp = mention_data["timestamp"]
                        reason = mention_data.get("reason")
                        if reason:
                            await message.channel.send(
                                embed=disnake.Embed(
                                    description=f"{member.mention} is AFK: `{reason}` <t:{timestamp}:R>",
                                    color=message.author.top_role.color,
                                ),
                                allowed_mentions=disnake.AllowedMentions(
                                    everyone=False, users=False, roles=False
                                ),
                            )

                        if not reason:
                            await message.channel.send(
                                embed=disnake.Embed(
                                    description=f"{member.mention} is AFK. Since <t:{timestamp}:R>",
                                    color=message.author.top_role.color,
                                ),
                                allowed_mentions=disnake.AllowedMentions(
                                    everyone=False, users=False, roles=False
                                ),
                            )
                    else:
                        break
                else:
                    break

    @commands.command()
    async def editsnipe(self, ctx: commands.Context):

        """Snipes most recently edited message."""

        try:
            if self.before.guild.id == ctx.guild.id:
                if self.before.channel.id == ctx.channel.id:

                    before = disnake.Embed(
                        description=f"{self.before.content}",
                        timestamp=datetime.utcnow(),
                        color=disnake.Color.blurple(),
                    )
                    before.set_footer(text=f"Message from {self.before.author}")
                    before.set_author(
                        name=f"{self.before.author}",
                        icon_url=self.before.author.display_avatar,
                    )
                    await ctx.send(embed=before)

        except Exception:
            await ctx.send(
                "There currently are no recently edited messages.",
            )

    @commands.command()
    async def snipe(self, ctx: commands.Context):
        """Snipes most recently deleted message."""

        try:
            if self.snipe_cache.guild.id == ctx.guild.id:
                if self.snipe_cache.channel.id == ctx.channel.id:

                    embed = disnake.Embed(
                        description=f"{self.snipe_cache.content}",
                        timestamp=datetime.utcnow(),
                        color=disnake.Color.blurple(),
                    )
                    embed.set_footer(text=f"Message from {self.snipe_cache.author}")
                    embed.set_author(
                        name=f"{self.snipe_cache.author}",
                        icon_url=self.snipe_cache.author.display_avatar,
                    )
                    await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(
                "No message was deleted, or the message was not in my cache.",
            )
            print(e)

    @commands.command(help="Gives a joke.")
    async def joke(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/joke") as r:
                data = await r.json(content_type=None)
                await ctx.send(data["joke"])

    @commands.slash_command()
    async def base64(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @base64.sub_command()
    async def encode(
        self,
        inter: disnake.ApplicationCommandInteraction,
        argument: str = commands.Param(description="A string"),
    ):
        """Encodes a message into a base64 string"""
        try:
            await inter.response.send_message(
                self.b64_encode(argument), ephemeral=False
            )
        except Exception:
            await inter.response.send_message(
                f"Couldn't encode that message.", ephemeral=False
            )

    @base64.sub_command()
    async def decode(
        self,
        inter: disnake.ApplicationCommandInteraction,
        argument: str = commands.Param(description="The base64 string"),
    ):
        """Decodes a base64 string"""
        try:
            await inter.response.send_message(
                self.b64_decode(argument), ephemeral=False
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
                f"&format=json&list=search&utf8=1&srsearch={query}&srlimit=5&srprop="
            )
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
                        f"&inprop=url&titles={article}"
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
                    title=f"**{article}**",
                    url=arturl,
                    description=artdesc,
                    color=0x3FCAFF,
                    timestamp=datetime.utcnow(),
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
                await ctx.send(embed=embed)

    @commands.slash_command(name="wikipedia")
    async def wikipedia_slash(
        self, inter: disnake.ApplicationCommandInteraction, query: str
    ):
        """Searches for something on the wikipedia"""
        async with self.bot.session.get(
            (
                "https://en.wikipedia.org//w/api.php?action=query"
                f"&format=json&list=search&utf8=1&srsearch={query}&srlimit=5&srprop="
            )
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
                        f"&inprop=url&titles={query}"
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
                    title=f"**{article}**",
                    url=arturl,
                    description=artdesc,
                    color=0x3FCAFF,
                    timestamp=datetime.utcnow(),
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
                await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="minecraft")
    async def minecraft(self, ctx: commands.Context, username=None):
        """Gets information about a minecraft user!"""

        if username is None:
            return await ctx.send()

        async with self.bot.session.get(
            f"https://api.mojang.com/users/profiles/minecraft/{username}"
        ) as r:

            uuid = (await r.json())["id"]

        async with self.bot.session.get(
            f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        ) as r:

            value = (await r.json())["properties"][0]["value"]

        url = json.loads(base64.b64decode(value).decode("utf-8"))["textures"]["SKIN"][
            "url"
        ]

        async with self.bot.session.get(
            f"https://api.mojang.com/user/profiles/{uuid}/names"
        ) as r:

            names = await r.json()

        history = []

        for name in reversed(names):
            history.append(name["name"])

        embed = disnake.Embed(
            title=f"{username}",
            color=disnake.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.add_field(name="Username", value=username)
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.add_field(name="Name History", value=", ".join(history))
        embed.set_thumbnail(url=url)
        embed.set_footer(icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)

    @commands.command(name="kiss", help="Kiss a user!")
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
        """Kiss a user!"""
        await inter.response.send_message(
            f"{inter.author.mention} kissed {member.mention}!!\nhttps://tenor.com/view/milk-and-mocha-bear-couple-kisses-kiss-love-gif-12498627",
            ephemeral=False,
        )

    @commands.command(name="bonk")
    @commands.guild_only()
    async def bonk_cmd(self, ctx: commands.Context, member: disnake.Member):
        """Bonk a user!"""
        bonkis = [
            "https://tenor.com/view/despicable-me-minions-bonk-hitting-cute-gif-17663380",
            "https://tenor.com/view/lol-gif-21667170",
            "https://tenor.com/view/azura-bonk-azura-bonk-gif-21733152",
        ]
        bonkiuwu = random.choice(bonkis)
        await ctx.send(f"{ctx.author.mention} bonked {member.mention}!\n{bonkiuwu}")

    @commands.slash_command(name="bonk")
    @commands.guild_only()
    async def bonk_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Bonk a user!"""
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

    @commands.command(name="spank")
    @commands.guild_only()
    async def spank_cmd(self, ctx: commands.Context, member: disnake.Member):
        """Spank a user!"""
        await ctx.send(
            f"{ctx.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590"
        )

    @commands.slash_command(name="spank")
    @commands.guild_only()
    async def spank_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Spank a user!"""
        await inter.response.send_message(
            f"{inter.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590",
            ephemeral=False,
        )

    @commands.command(name="slap")
    @commands.guild_only()
    async def slap_cmd(self, ctx: commands.Context, member: disnake.Member):
        """Slap a user!"""
        await ctx.send(
            f"{ctx.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299"
        )

    @commands.slash_command(name="slap")
    @commands.guild_only()
    async def slap_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Slap a user!"""
        await inter.response.send_message(
            f"{inter.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299",
            ephemeral=False,
        )

    @commands.command(name="pat")
    @commands.guild_only()
    async def pat(self, ctx: commands.Context, member: disnake.Member):
        """Pat a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                data = await r.json(content_type=None)
                image = data["link"]
                await ctx.send(
                    f"{ctx.author.mention} patted {member.mention}!!\n{image}"
                )

    @commands.slash_command(name="pat")
    @commands.guild_only()
    async def pat_slash(
        self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member
    ):
        """Pat a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                data = await r.json()
                image = data["link"]
                await inter.response.send_message(
                    f"{inter.author.mention} patted {member.mention}!!\n{image}",
                    ephemeral=False,
                )

    @commands.command(name="cat")
    async def cat(self, ctx: commands.Context) -> None:
        """Sends a random cat image."""
        async with ctx.typing():
            async with self.bot.session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    data = await r.json()
                    await ctx.send(
                        embed=disnake.Embed(color=disnake.Color.greyple()).set_image(
                            url=data["file"]
                        )
                    )

    @commands.slash_command(name="cat")
    async def cat_slash(self, inter: disnake.ApplicationCommandInteraction) -> None:
        """Sends a random cat image"""
        async with self.bot.session.get("http://aws.random.cat/meow") as r:
            if r.status == 200:
                data = await r.json()
                await inter.response.send_message(
                    embed=disnake.Embed(color=disnake.Color.greyple()).set_image(
                        url=data["file"]
                    ),
                    ephemeral=False,
                )

    @commands.command(name="dog")
    async def dog(self, ctx: commands.Context):
        """Sends a random dog image."""
        async with ctx.typing():
            async with self.bot.session.get(
                "https://dog.ceo/api/breeds/image/random"
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    await ctx.send(
                        embed=disnake.Embed(color=disnake.Color.greyple()).set_image(
                            url=data["message"]
                        )
                    )

    @commands.slash_command(name="dog")
    async def dog_slash(self, inter: disnake.ApplicationCommandInteraction):
        """Sends a random dog image"""
        async with self.botsession.get("https://dog.ceo/api/breeds/image/random") as r:
            if r.status == 200:
                data = await r.json()

                await inter.response.send_message(
                    embed=disnake.Embed(color=disnake.Color.greyple()).set_image(
                        url=data["message"]
                    ),
                    ephemeral=False,
                )

    @commands.command(name="hug")
    @commands.guild_only()
    async def hug_cmd(self, ctx: commands.Context, member: disnake.Member):
        """Hug a user!"""
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
        """Hug a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                data = await r.json()
                image = data["link"]
                await inter.response.send_message(
                    f"{inter.author.mention} hugged {member.mention}!!\n{image}"
                )

    async def get_urban_response(self, ctx: commands.Context, term: str):

        headers = {
            "x-rapidapi-host": os.environ.get("x_host"),
            "x-rapidapi-key": os.environ.get("x_key"),
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                url="https://mashape-community-urban-dictionary.p.rapidapi.com/define",
                params={"term": term},
            ) as response:
                try:
                    data = await response.json()

                    definition, embeds = [], []

                    for item in data["list"]:
                        definition.append(
                            f'{item["word"]}\n\n**Definition:** {item["definition"]}\n\n**Author:**\n{item["author"]}'
                        )

                    for name in definition:
                        emb = disnake.Embed(
                            description=name, color=disnake.Color.greyple()
                        )
                        embeds.append(emb)

                    await ctx.send(
                        embed=embeds[0],
                        view=utils.Paginator(ctx, embeds, embed=True),
                    )
                except IndexError:
                    return await ctx.send(
                        embed=disnake.Embed(
                            description="No definitions found for that word.",
                            color=disnake.Color.red(),
                        )
                    )

    @commands.command()
    async def define(self, ctx: commands.Context, term: str):
        """Show's a meaning of a word."""
        await self.get_urban_response(ctx, term)

    @commands.command()
    async def afk(self, ctx: commands.Context, *, reason: Optional[str]):
        """Become AFK."""

        afk_db = self.afk[str(ctx.guild.id)]

        data = await afk_db.find_one({"_id": ctx.author.id})

        if not data:
            if reason:
                await afk_db.insert_one(
                    {
                        "_id": ctx.author.id,
                        "reason": reason,
                        "timestamp": int(datetime.utcnow().timestamp()),
                        "message": ctx.message.id,
                    }
                )
                await ctx.send(
                    embed=disnake.Embed(
                        description="You are now AFK.", color=ctx.author.top_role.color
                    )
                )
                return

            await afk_db.insert_one(
                {"_id": ctx.author.id, "timestamp": int(datetime.utcnow().timestamp())}
            )
            await ctx.send(
                embed=disnake.Embed(
                    description="You are now AFK.", color=ctx.author.top_role.color
                )
            )
        else:
            return

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:

        """Returns the bots latency."""

        embed = disnake.Embed(
            description=f"**Ponged!** {self.bot.latency * 1000:.2f}ms",
            color=disnake.Color.blurple(),
        )

        await ctx.reply(embed=embed, mention_author=False)

    @commands.slash_command(name="ping")
    async def ping_slash(self, inter: disnake.ApplicationCommandInteraction) -> None:

        """Returns the bots latency"""

        embed = disnake.Embed(
            description=f"**Ponged!** {self.bot.latency * 1000:.2f}ms",
            color=disnake.Color.blurple(),
        )

        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.command()
    async def choose(self, ctx: commands.Context, *args):

        """Chooses between multiple choices."""

        await ctx.send(random.choice(args))

    @commands.command(name="calculator", aliases=["calc"])
    async def calculator(self, ctx: commands.Context):
        view = utils.Calculator()
        await ctx.send("Click a button!", view=view)


def setup(bot):
    bot.add_cog(General(bot))
