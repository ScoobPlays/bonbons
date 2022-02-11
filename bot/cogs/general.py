import base64
import json
import os
import random
from datetime import datetime
from typing import Optional

import aiohttp
from disnake import (AllowedMentions, ApplicationCommandInteraction, Color,
                     Embed, Member, Message, TextChannel, File)
from disnake.ext.commands import (Cog, Context, Param, command, guild_only,
                                  slash_command, group)

from utils import Calculator, Paginator
from simpleeval import simple_eval, FeatureNotAvailable
from io import BytesIO

class General(Cog, description="General commands."):
    def __init__(self, bot):
        self.bot = bot
        self._snipe_cache = []
        self._edit_cache = []
        self.emoji = "🙌"
        self.afk = self.bot.mongo["discord"]["afk"]

    @staticmethod
    def base64_encode(text: str):
        message_bytes = text.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        message = base64_bytes.decode("ascii")
        return message

    @staticmethod
    def base64_decode(text: str):
        b64msg = text.encode("ascii")
        message_bytes = base64.b64decode(b64msg)
        message = message_bytes.decode("ascii")
        return message

      
      
    @group(name="base64", aliases=["b64"], invoke_without_command=True, case_insensitive=True)
    async def base64_group(self, ctx: Context):

        """
        The base command for base64.
        """

        await ctx.send_help("base64")

    @base64_group.command()
    async def encode(self, ctx: Context, *, string: str):

        """
        Encodes a string.
        """
        
        try:
            return await ctx.send(self.base64_encode(string))
        except Exception:
            return await ctx.send(f"Could not encode '{string}'.")

    @base64_group.command()
    async def decode(self, ctx: Context, *, string: str):

        """
        Decodes a base64 string
        """
        
        try:
            return await ctx.send(self.base64_decode(string))

        except Exception:
            return await ctx.send(f"Could not decode '{string}'.")

    @Cog.listener()
    async def on_message_delete(self, message: Message):

        if message.author.bot:
            return

        if not isinstance(message.channel, TextChannel):
            return

        self._snipe_cache.append(
            {"author": str(message.author), "channel": message.channel.id, "content": message.content, "timestamp": datetime.utcnow(), "msg": message}
        ) 

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):

        if after.author.bot:
            return

        self._edit_cache.append(
            {"author": str(before.author), "channel": before.channel.id, "content": before.content, "timestamp": datetime.utcnow(), "msg": before}
        ) 

    @Cog.listener()
    async def on_message(self, message: Message):
        
        if not isinstance(message.channel, TextChannel):
            return

        if message.author.bot:
            return

        afk_db = self.afk[str(message.guild.id)]

        data = await afk_db.find_one({"_id": message.author.id})

        if data:
            await message.channel.send(
                embed=Embed(
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
                                embed=Embed(
                                    description=f"{member.mention} is AFK: `{reason}` <t:{timestamp}:R>",
                                    color=message.author.top_role.color,
                                ),
                                allowed_mentions=AllowedMentions(
                                    everyone=False, users=False, roles=False
                                ),
                            )

                        if not reason:
                            await message.channel.send(
                                embed=Embed(
                                    description=f"{member.mention} is AFK. Since <t:{timestamp}:R>",
                                    color=message.author.top_role.color,
                                ),
                                allowed_mentions=AllowedMentions(
                                    everyone=False, users=False, roles=False
                                ),
                            )
                    else:
                        break
                else:
                    break

    @command()
    async def editsnipe(self, ctx: Context, id: int=None):

        """Tells you most recently edited message."""

        if len(self._edit_cache) == 0:
            return await ctx.send("There currently are no recently edited messages.")

        try:
            message = self._edit_cache[id]
        except Exception:
            message = self._edit_cache[-1]

        if message["channel"] == ctx.channel.id:

                    embed = Embed(
                        description=message["content"],
                        timestamp=message["timestamp"],
                        color=Color.blurple(),
                    )
                    embed.set_footer(text=f"Message edited at")
                    embed.set_author(
                        name=message["author"],
                        icon_url=message["msg"].author.display_avatar.url,
                    )
                    return await ctx.send(embed=embed)



    @command()
    async def snipe(self, ctx: Context, id: int=None):
       
        """Tells you the most recently deleted message."""

        if len(self._snipe_cache) == 0:
            return await ctx.send("No message was deleted, or the message was not in my cache.")

        try:
            message = self._snipe_cache[id]
        except Exception:
            message = self._snipe_cache[-1]

        if message["channel"] == ctx.channel.id:

                    embed = Embed(
                        description=message["content"],
                        timestamp=message["timestamp"],
                        color=Color.blurple(),
                    )
                    embed.set_footer(text=f"Message deleted at")
                    embed.set_author(
                        name=message["author"],
                        icon_url=message["msg"].author.display_avatar.url,
                    )
                    return await ctx.send(embed=embed)

    @command()
    async def joke(self, ctx: Context):

        """Tells you a random joke!"""

        async with self.bot.session.get("https://some-random-api.ml/joke") as payload:
            data = await payload.json(content_type=None)
            return await ctx.send(data["joke"])

    @command(name="wikipedia", aliases=("wiki",))
    async def wikipedia_cmd(self, ctx: Context, *, query: str):
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
                embed = Embed(
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


    @command(name="minecraft")
    async def minecraft(self, ctx: Context, username=None):
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

        embed = Embed(
            title=f"{username}",
            color=Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.add_field(name="Username", value=username)
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.add_field(name="Name History", value=", ".join(history))
        embed.set_thumbnail(url=url)
        embed.set_footer(icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)

    @command(name="kiss", help="Kiss a user!")
    @guild_only()
    async def kiss_cmd(self, ctx: Context, member: Member):
        await ctx.send(
            f"{ctx.author.mention} kissed {member.mention}!!\nhttps://tenor.com/view/milk-and-mocha-bear-couple-kisses-kiss-love-gif-12498627"
        )


    @command(name="bonk")
    @guild_only()
    async def bonk_cmd(self, ctx: Context, member: Member):
        """Bonk a user!"""
        bonkis = [
            "https://tenor.com/view/despicable-me-minions-bonk-hitting-cute-gif-17663380",
            "https://tenor.com/view/lol-gif-21667170",
            "https://tenor.com/view/azura-bonk-azura-bonk-gif-21733152",
        ]
        bonkiuwu = random.choice(bonkis)
        await ctx.send(f"{ctx.author.mention} bonked {member.mention}!\n{bonkiuwu}")

    @command(name="spank")
    @guild_only()
    async def spank_cmd(self, ctx: Context, member: Member):
        """Spank a user!"""
        await ctx.send(
            f"{ctx.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590"
        )

    @command(name="slap")
    @guild_only()
    async def slap_cmd(self, ctx: Context, member: Member):
        """Slap a user!"""
        await ctx.send(
            f"{ctx.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299"
        )

    @command(name="pat")
    @guild_only()
    async def pat(self, ctx: Context, member: Member):
        """Pat a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                data = await r.json(content_type=None)
                image = data["link"]
                await ctx.send(
                    f"{ctx.author.mention} patted {member.mention}!!\n{image}"
                )

    @command(name="cat")
    async def cat(self, ctx: Context) -> None:
        """Sends a random cat image."""
        async with ctx.typing():
            async with self.bot.session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    data = await r.json()
                    await ctx.send(
                        embed=Embed(color=Color.blurple()).set_image(url=data["file"])
                    )


    @command(name="dog")
    async def dog(self, ctx: Context):
        """Sends a random dog image."""
        async with ctx.typing():
            async with self.bot.session.get(
                "https://dog.ceo/api/breeds/image/random"
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    await ctx.send(
                        embed=Embed(color=Color.blurple()).set_image(
                            url=data["message"]
                        )
                    )


    @command(name="hug")
    @guild_only()
    async def hug_cmd(self, ctx: Context, member: Member):
        """Hug a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                data = await r.json()
                image = data["link"]
                await ctx.send(
                    f"{ctx.author.mention} hugged {member.mention}!!\n{image}"
                )
                
    async def get_urban_response(self, ctx: Context, term: str):

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
                        emb = Embed(description=name, color=Color.blurple())
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

    @command()
    async def define(self, ctx: Context, term: str):
        """Show's a meaning of a word."""
        await self.get_urban_response(ctx, term)

    @command()
    async def afk(self, ctx: Context, *, reason: Optional[str]=None):
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
                    embed=Embed(
                        description="You are now AFK.", color=ctx.author.top_role.color
                    )
                )
                return

            await afk_db.insert_one(
                {"_id": ctx.author.id, "timestamp": int(datetime.utcnow().timestamp()), "message": ctx.message.id}
            )
            await ctx.send(
                embed=Embed(
                    description="You are now AFK.", color=ctx.author.top_role.color
                )
            )
        else:
            return
            
    @command()
    async def choose(self, ctx: Context, *args):

        """Chooses between multiple choices."""

        await ctx.send(random.choice(args))

    @command(name="bcalc", aliases=["bcalculator"])
    async def button_calculator(self, ctx: Context):

        """
        A custom calculator made using buttons.
        """

        view =Calculator()
        await ctx.send("Click a button!", view=view)

    @staticmethod
    def parse_expressions(expressions: str):
        return expressions.replace("^", "**")
        
    @command(name="calc")
    async def calc(self, ctx: Context, *, expressions: str):

        """
        Tells you the result of expressions.
        """

        try:
            result = simple_eval(self.parse_expressions(expressions))
            
            if len(str(result)) >= 500:
                result = f"{result: ,}"
                buffer = BytesIO(result.encode("utf-8"))
                file = File(buffer, "result.txt")
                await ctx.send(f"The result was too big (`{len(result.replace(',', ''))}`), sending it to your DMs now..")
                return await ctx.author.send(file = file)
            
            return await ctx.send(f"Result:`{result:,}`")
        
        except:
            return await ctx.send("I could not evalute expression your expression(s).")


def setup(bot):
    bot.add_cog(General(bot))
