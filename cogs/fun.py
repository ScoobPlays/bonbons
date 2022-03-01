import base64
import json
import os
import random
from datetime import datetime
from io import BytesIO
from typing import Optional

import aiohttp
import discord
from discord.ext import commands
from discord.ui import View, button
from simpleeval import simple_eval

from utils.bot import Bonbons
from utils.paginator import Paginator


class Calculator(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.string = "Click a button!"

    @button(label="1", custom_id="calc:one")
    async def calc_one(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(1)
        await inter.edit_original_message(content=new)

    @button(label="2", custom_id="calc:two")
    async def calc_two(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(2)
        await inter.edit_original_message(content=new)

    @button(label="3", custom_id="calc:three")
    async def calc_three(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(3)
        await inter.edit_original_message(content=new)

    @button(label="4", row=1, custom_id="calc:four")
    async def calc_four(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(4)
        await inter.edit_original_message(content=new)

    @button(label="5", row=1, custom_id="calc:five")
    async def calc_five(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(5)
        await inter.edit_original_message(content=new)

    @button(label="6", row=1, custom_id="calc:six")
    async def calc_six(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(6)
        await inter.edit_original_message(content=new)

    @button(label="7", row=2, custom_id="calc:seven")
    async def calc_seven(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(7)
        await inter.edit_original_message(content=new)

    @button(label="8", row=2, custom_id="calc:eight")
    async def calc_eight(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(8)
        await inter.edit_original_message(content=new)

    @button(label="9", row=2, custom_id="calc:nine")
    async def calc_nine(self, button, inter):
        await inter.response.defer()
        data = (inter.message.content).replace(self.string, "")
        new = data + str(9)
        await inter.edit_original_message(content=new)

    @button(label="+", style=discord.ButtonStyle.blurple, row=0, custom_id="calc:plus")
    async def plus(self, button, inter):

        if inter.message.content == self.string:
            return await inter.response.send_message(
                "What are you trying to do?", ephemeral=True
            )

        await inter.response.defer()

        data = (inter.message.content).replace(self.string, "")

        new_plus = data.count("+")
        if new_plus >= 1:
            return await inter.response.send_message(
                "You cannot have more than one operator in a message."
            )

        new = data + str("+")
        await inter.edit_original_message(content=new)

    @button(
        label="*", style=discord.ButtonStyle.blurple, row=1, custom_id="calc:multiply"
    )
    async def multiply(self, button, inter):
        if inter.message.content == self.string:
            return await inter.response.send_message(
                "What are you trying to do?", ephemeral=True
            )

        await inter.response.defer()

        data = (inter.message.content).replace(self.string, "")
        new_plus = data.count("*")

        if new_plus >= 1:
            return await inter.response.send_message(
                "You cannot have more than one operator in a message."
            )

        new = data + str("*")
        await inter.edit_original_message(content=new)

    @button(
        label="=", style=discord.ButtonStyle.blurple, row=2, custom_id="calc:equals"
    )
    async def equals(self, button, inter):
        await inter.response.defer()
        new = eval(inter.message.content)
        await inter.edit_original_message(content=new)

    @button(label="Clear", style=discord.ButtonStyle.red, row=3, custom_id="calc:clear")
    async def clear(self, button, inter):
        await inter.response.defer()
        await inter.edit_original_message(content=self.string)

    @button(label="Stop", style=discord.ButtonStyle.red, row=3, custom_id="calc:stop")
    async def stop(self, button, inter):
        await inter.response.defer()

        for children in self.children:
            children.disabled = True

        await inter.edit_original_message(view=self)


class Fun(commands.Cog):
    """
    Fun commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self._snipe_cache = []
        self._edit_cache = []
        self.afk = self.bot.mongo["discord"]["afk"]

    @property
    def emoji(self) -> str:
        return "🙌"

    def base64_encode(self, text: str):
        message_bytes = text.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        message = base64_bytes.decode("ascii")
        return message

    def base64_decode(self, text: str):
        b64msg = text.encode("ascii")
        message_bytes = base64.b64decode(b64msg)
        message = message_bytes.decode("ascii")
        return message

    @commands.group(
        name="base64",
        aliases=["b64"],
        invoke_without_command=True,
        case_insensitive=True,
    )
    async def base64_group(self, ctx: commands.Context) -> None:

        """
        The base command for base64.
        """

        await ctx.send_help("base64")

    @base64_group.command()
    async def encode(self, ctx: commands.Context, *, string: str) -> None:

        """
        Encodes a string.
        """

        try:
            return await ctx.send(self.base64_encode(string))
        except Exception:
            return await ctx.send(f"Could not encode string.")

    @base64_group.command()
    async def decode(self, ctx: commands.Context, *, string: str) -> None:

        """
        Decodes a base64 string
        """

        try:
            return await ctx.send(self.base64_decode(string))

        except Exception:
            return await ctx.send(f"Could not decode string.")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:

        if message.author.bot:
            return

        if not isinstance(message.channel, discord.TextChannel):
            return

        self._snipe_cache.append(
            {
                "author": str(message.author),
                "channel": message.channel.id,
                "content": message.content,
                "timestamp": datetime.utcnow(),
                "msg": message,
            }
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):

        if after.author.bot:
            return

        self._edit_cache.append(
            {
                "author": str(before.author),
                "channel": before.channel.id,
                "content": before.content,
                "timestamp": datetime.utcnow(),
                "msg": before,
            }
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        if not isinstance(message.channel, discord.TextChannel):
            return

        if message.author.bot:
            return

        afk_db = self.afk[str(message.guild.id)]

        data = await afk_db.find_one({"_id": message.author.id})

        if data:
            await message.channel.send(
                embed=discord.Embed(
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
                                embed=discord.Embed(
                                    description=f"{member.mention} is AFK: `{reason}` <t:{timestamp}:R>",
                                    color=message.author.top_role.color,
                                ),
                                allowed_mentions=discord.AllowedMentions(
                                    everyone=False, users=False, roles=False
                                ),
                            )

                        if not reason:
                            await message.channel.send(
                                embed=discord.Embed(
                                    description=f"{member.mention} is AFK. Since <t:{timestamp}:R>",
                                    color=message.author.top_role.color,
                                ),
                                allowed_mentions=discord.AllowedMentions(
                                    everyone=False, users=False, roles=False
                                ),
                            )
                    else:
                        break
                else:
                    break

    @commands.command()
    async def editsnipe(self, ctx: commands.Context, id: int = None):

        """Tells you most recently edited message."""

        if len(self._edit_cache) == 0:
            return await ctx.send("There currently are no recently edited messages.")

        try:
            message = self._edit_cache[id]
        except Exception:
            message = self._edit_cache[-1]

        if message["channel"] == ctx.channel.id:

            embed = discord.Embed(
                description=message["content"],
                timestamp=message["timestamp"],
                color=discord.Color.blurple(),
            )
            embed.set_footer(text=f"Message edited at")
            embed.set_author(
                name=message["author"],
                icon_url=message["msg"].author.display_avatar.url,
            )
            return await ctx.send(embed=embed)

    @commands.command()
    async def snipe(self, ctx: commands.Context, id: int = None):

        """Tells you the most recently deleted message."""

        if len(self._snipe_cache) == 0:
            return await ctx.send(
                "No message was deleted, or the message was not in my cache."
            )

        try:
            message = self._snipe_cache[id]
        except Exception:
            message = self._snipe_cache[-1]

        if message["channel"] == ctx.channel.id:

            embed = discord.Embed(
                description=message["content"],
                timestamp=message["timestamp"],
                color=discord.Color.blurple(),
            )
            embed.set_footer(text=f"Message deleted at")
            embed.set_author(
                name=message["author"],
                icon_url=message["msg"].author.display_avatar.url,
            )
            return await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx: commands.Context) -> None:

        """Tells you a random joke!"""

        async with self.bot.session.get("https://some-random-api.ml/joke") as payload:
            data = await payload.json(content_type=None)
            return await ctx.send(data["joke"])

    @commands.command(name="wikipedia", aliases=("wiki",))
    async def wikipedia_cmd(self, ctx: commands.Context, *, query: str) -> None:
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
                embed = discord.discord.Embed(
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

    @commands.command(name="kiss", help="Kiss a user!")
    @commands.guild_only()
    async def kiss_cmd(self, ctx: commands.Context, member: discord.Member):
        await ctx.send(
            f"{ctx.author.mention} kissed {member.mention}!!\nhttps://tenor.com/view/milk-and-mocha-bear-couple-kisses-kiss-love-gif-12498627"
        )

    @commands.command(name="bonk")
    @commands.guild_only()
    async def bonk_cmd(self, ctx: commands.Context, member: discord.Member):
        """Bonk a user!"""
        bonkis = [
            "https://tenor.com/view/despicable-me-minions-bonk-hitting-cute-gif-17663380",
            "https://tenor.com/view/lol-gif-21667170",
            "https://tenor.com/view/azura-bonk-azura-bonk-gif-21733152",
        ]
        bonkiuwu = random.choice(bonkis)
        await ctx.send(f"{ctx.author.mention} bonked {member.mention}!\n{bonkiuwu}")

    @commands.command(name="spank")
    @commands.guild_only()
    async def spank_cmd(self, ctx: commands.Context, member: discord.Member):
        """Spank a user!"""
        await ctx.send(
            f"{ctx.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590"
        )

    @commands.command(name="slap")
    @commands.guild_only()
    async def slap_cmd(self, ctx: commands.Context, member: discord.Member):
        """Slap a user!"""
        await ctx.send(
            f"{ctx.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299"
        )

    @commands.command(name="pat")
    @commands.guild_only()
    async def pat(self, ctx: commands.Context, member: discord.Member):
        """Pat a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                data = await r.json(content_type=None)
                image = data["link"]
                await ctx.send(
                    f"{ctx.author.mention} patted {member.mention}!!\n{image}"
                )

    @commands.command(name="cat")
    async def cat(self, ctx: commands.Context) -> None:
        """Sends a random cat image."""
        async with ctx.typing():
            async with self.bot.session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    data = await r.json()
                    await ctx.send(
                        embed=discord.Embed(color=discord.Color.blurple()).set_image(
                            url=data["file"]
                        )
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
                        embed=discord.Embed(color=discord.Color.blurple()).set_image(
                            url=data["message"]
                        )
                    )

    @commands.command(name="hug")
    @commands.guild_only()
    async def hug_cmd(self, ctx: commands.Context, member: discord.Member) -> None:
        """Hug a user!"""
        async with self.bot.session.get("https://some-random-api.ml/animu/hug") as r:
            data = await r.json()
            image = data["link"]
            await ctx.send(f"{ctx.author.mention} hugged {member.mention}!!\n{image}")

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
                        emb = discord.Embed(
                            description=name, color=discord.Color.blurple()
                        )
                        embeds.append(emb)

                    view = Paginator(ctx, embeds, embed=True)
                    view.msg = await ctx.send(
                        embed=embeds[0],
                        view=view,
                    )
                except IndexError:
                    return await ctx.send(
                        "Well, there were no definitions for that word. Maybe you can go and make one for it?"
                    )

    @commands.command()
    async def define(self, ctx: commands.Context, term: str):
        """Show's a meaning of a word."""
        await self.get_urban_response(ctx, term)

    @commands.command()
    async def afk(self, ctx: commands.Context, *, reason: Optional[str] = None):
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
                    embed=discord.Embed(
                        description="You are now AFK.", color=ctx.author.top_role.color
                    )
                )
                return

            await afk_db.insert_one(
                {
                    "_id": ctx.author.id,
                    "timestamp": int(datetime.utcnow().timestamp()),
                    "message": ctx.message.id,
                }
            )
            await ctx.send(
                embed=discord.Embed(
                    description="You are now AFK.", color=ctx.author.top_role.color
                )
            )
        else:
            return

    @commands.command()
    async def choose(self, ctx: commands.Context, *args) -> None:

        """Chooses between multiple choices."""

        await ctx.send(random.choice(args))

    @commands.command(name="bcalc", aliases=["bcalculator"])
    async def button_calculator(self, ctx: commands.Context) -> None:

        """
        A custom calculator made using buttons.
        """

        view = Calculator()
        await ctx.send("Click a button!", view=view)

    def parse_expressions(self, expressions: str) -> str:
        return expressions.replace("^", "**")

    @commands.command(name="calc")
    async def calc(self, ctx: commands.Context, *, expressions: str) -> None:

        """
        Tells you the result of expressions.
        """

        try:
            result = simple_eval(self.parse_expressions(expressions))

            if len(str(result)) >= 100:
                buffer = BytesIO(str(result).encode("utf-8"))
                file = discord.File(buffer, "result.txt")
                await ctx.send(
                    f"The result was too big (`{len(str(result)):,)}`), sending it to your DMs now.."
                )
                return await ctx.author.send(file=file)

            return await ctx.send(f"Result: `{result}`")

        except:
            return await ctx.send("I could not evalute expression your expression(s).")

    @commands.command(name="meme")
    async def meme(self, ctx: commands.Context) -> None:
        """
        Sends a random meme.
        """

        if self.bot.memes == []:
            return await ctx.reply("Memes have not yet been cached. Please wait a couple of seconds.")
        
        meme = random.choice(self.bot.memes)

        embed = discord.Embed(title=meme.title, color=discord.Color.random())
        embed.set_image(url=meme.url)

        await ctx.send(embed=embed)

def setup(bot: Bonbons) -> None:
    bot.add_cog(Fun(bot))
