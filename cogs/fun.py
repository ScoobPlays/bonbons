from datetime import datetime
from disnake import (
    Embed,
    Member,
    Message,
    ui,
    ButtonStyle,
    Color,
    Interaction,
    ApplicationCommandInteraction,
    Forbidden
    )
from disnake.ext import commands
import json
import base64
import random
import aiohttp
import contextlib
from utils.utils import Google


class Fun(commands.Cog, description="Random commands."):
    def __init__(self, bot):
        self.bot = bot
        self.last_msg = None
        self.before = None
        self.after = None

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
    async def on_message_delete(self, message:  Message):

        if message.author.bot:
            return

        self.last_msg = message

    @commands.Cog.listener()
    async def on_message_edit(self, before: str, after: str):

        if before.author.bot or after.author.bot:
            return

        self.before = before
        self.after = after

    @commands.command()
    async def editsnipe(self, ctx: commands.Context):
        
        """Snipes most recently edited message."""

        message = ctx.message
        try:
            if self.before.guild.id == ctx.guild.id:
                if self.before.channel.id == ctx.channel.id:

                    before =  Embed(
                        description=f"{self.before.content}",
                        timestamp=datetime.utcnow(),
                    )
                    before.set_footer(text=f"Message from {self.before.author}")
                    before.set_author(
                        name=f"{self.before.author}",
                        icon_url=self.before.author.display_avatar,
                    )

                    after = Embed(
                        description=f"{self.after.content}", timestamp=datetime.utcnow()
                    )
                    after.set_footer(text=f"Message from {self.after.author}")
                    after.set_author(
                        name=f"{self.after.author}",
                        icon_url=self.after.author.display_avatar,
                    )

                    class Edit(ui.View):
                        def __init__(self):
                            super().__init__()

                        async def interaction_check(
                            self, interaction: Interaction
                        ) -> bool:
                            if (
                                interaction.user
                                and interaction.user.id == ctx.author.id
                            ):
                                return True
                            await interaction.response.send_message(
                                "You are not the owner of this message.", ephemeral=True
                            )
                            return False

                        @ui.button(
                            label="Before", style=ButtonStyle.grey
                        )
                        async def before(self, button, inter):
                            await msg.edit(embed=before)
                            await inter.response.defer()

                        @ui.button(
                            label="After", style=ButtonStyle.grey
                        )
                        async def after(self, button, inter):
                            await msg.edit(embed=after)
                            await inter.response.defer()

                        @ui.button(label="Quit", style=ButtonStyle.red)
                        async def quit(self, button, inter):
                            await message.delete()
                            await inter.message.delete()

                    msg = await ctx.send(embed=before, view=Edit())

        except Exception:
            await ctx.send(
                embed=Embed(
                    description="There currently are no recently edited messages.",
                    color=Color.red(),
                )
            )

    @commands.command()
    async def snipe(self, ctx: commands.Context):
        message = ctx.message
        msg = self.last_msg
        """Snipes most recently deleted message."""

        try:
            if self.last_msg.guild.id == ctx.guild.id:
                if self.last_msg.channel.id == ctx.channel.id:

                    before = Embed(
                        description=f"{self.last_msg.content}",
                        timestamp=datetime.utcnow(),
                    )
                    before.set_footer(text=f"Message from {self.last_msg.author}")
                    before.set_author(
                        name=f"{self.last_msg.author}",
                        icon_url=self.last_msg.author.display_avatar,
                    )

                    class Edit(ui.View):
                        def __init__(self):
                            super().__init__()

                        async def interaction_check(
                            self, interaction: Interaction
                        ) -> bool:
                            if (
                                interaction.user
                                and interaction.user.id == ctx.author.id
                            ):
                                return True
                            await interaction.response.send_message(
                                "You are not the owner of this message.", ephemeral=True
                            )
                            return False

                        @ui.button(
                            label="Author", style=ButtonStyle.grey
                        )
                        async def before(self, button, inter):
                            await inter.response.send_message(
                                f"The author of this message is {msg.author.mention}.",
                                ephemeral=True,
                            )

                        @ui.button(
                            label="Channel", style=ButtonStyle.grey
                        )
                        async def after(self, button, inter):
                            await inter.response.send_message(
                                f"This message was deleted in {msg.channel.mention}.",
                                ephemeral=True,
                            )

                        @ui.button(label="Quit", style=ButtonStyle.red)
                        async def quit(self, button, inter):
                            await message.delete()
                            await inter.message.delete()

                    await ctx.send(embed=before, view=Edit())

        except Exception:
            await ctx.send(
                embed=Embed(
                    description="There currently are no recently deleted messages.",
                    color=Color.red(),
                )
            )

    @commands.command(help="Gives a joke.")
    async def joke(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/joke") as r:
                data = await r.json()
                await ctx.send(data["joke"])

    @commands.command(name="google")
    async def google(self, ctx: commands.Context, *, query: str):

        """Returns a google link for a query."""

        await ctx.send(f"Google Result for: `{query}`", view=Google(query))

    @commands.slash_command(name="google")
    async def google_slash(
        self, inter: ApplicationCommandInteraction, query: str
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
        self, inter: ApplicationCommandInteraction, argument: str
    ):
        "Says whatever you want for you"
        await inter.response.send_message(argument, ephemeral=False)

    @commands.slash_command()
    async def base64(self, inter: ApplicationCommandInteraction):
        pass

    @base64.sub_command()
    async def encode(self, inter: ApplicationCommandInteraction, argument: str):
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
    async def decode(self, inter: ApplicationCommandInteraction, argument: str):
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

    @commands.slash_command(name="wikipedia")
    async def wikipedia_slash(
        self, inter: ApplicationCommandInteraction, query: str
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
                await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="minecraft")
    async def minecraft(self, ctx: commands.Context, username="Notch"):
        """Fetches information about a minecraft user."""

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

        history = ""
        for name in reversed(names):
            history += name["name"] + "\n"

        embed = Embed(
            title=f"User Information For {username}", timestamp=datetime.utcnow()
        )
        embed.add_field(name="Username", value=username)
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.add_field(name="History", value=history)
        embed.set_thumbnail(url=url)
        embed.set_footer(icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)

    @commands.slash_command(name="minecraft")
    async def minecraft_slash(
        self, inter: ApplicationCommandInteraction, username="Notch"
    ):
        """Fetches information about a minecraft user."""

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

        history = ""
        for name in reversed(names):
            history += name["name"] + "\n"

        embed = Embed(
            title=f"User Information For {username}", timestamp=datetime.utcnow()
        )
        embed.add_field(name="Username", value=username)
        embed.set_author(name=inter.author, icon_url=inter.author.display_avatar)
        embed.add_field(name="History", value=history)
        embed.set_thumbnail(url=url)
        embed.set_footer(icon_url=inter.author.display_avatar)
        await inter.response.send_message(embed=embed, ephemeral=False)

    @commands.command(name="kiss", help="Kisses a user.")
    @commands.guild_only()
    async def kiss_cmd(self, ctx: commands.Context, member: Member):
        await ctx.send(
            f"{ctx.author.mention} kissed {member.mention}!!\nhttps://tenor.com/view/milk-and-mocha-bear-couple-kisses-kiss-love-gif-12498627"
        )

    @commands.slash_command(name="kiss")
    @commands.guild_only()
    async def kiss_slash(
        self, inter: ApplicationCommandInteraction, member: Member
    ):
        """Kisses a user"""
        await inter.response.send_message(
            f"{inter.author.mention} kissed {member.mention}!!\nhttps://tenor.com/view/milk-and-mocha-bear-couple-kisses-kiss-love-gif-12498627",
            ephemeral=False,
        )

    @commands.command(name="bonk", help="Bonks a user.")
    @commands.guild_only()
    async def bonk_cmd(self, ctx: commands.Context, member: Member):
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
        self, inter: ApplicationCommandInteraction, member: Member
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
    async def spank_cmd(self, ctx: commands.Context, member: Member):
        await ctx.send(
            f"{ctx.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590"
        )

    @commands.slash_command(name="spank", help="Spanks a user")
    @commands.guild_only()
    async def spank_slash(
        self, inter: ApplicationCommandInteraction, member: Member
    ):
        """Spanks a user"""
        await inter.response.send_message(
            f"{inter.author.mention} spanked {member.mention}!\nhttps://tenor.com/view/cats-funny-spank-slap-gif-15308590",
            ephemeral=False,
        )

    @commands.command(name="slap", help="Slaps a user.")
    @commands.guild_only()
    async def slap_cmd(self, ctx: commands.Context, member: Member):
        await ctx.send(
            f"{ctx.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299"
        )

    @commands.slash_command(name="slap")
    @commands.guild_only()
    async def slap_slash(
        self, inter: ApplicationCommandInteraction, member: Member
    ):
        """Slaps a user"""
        await inter.response.send_message(
            f"{inter.author.mention} slapped {member.mention}!\nhttps://tenor.com/view/slap-bear-slap-me-you-gif-17942299",
            ephemeral=False,
        )

    @commands.command(name="pat", help="Pats a user.")
    @commands.guild_only()
    async def pat_cmd(self, ctx: commands.Context, member: Member):
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
        self, inter: ApplicationCommandInteraction, member: Member
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
    async def hug_cmd(self, ctx: commands.Context, member: Member):
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
        self, inter: ApplicationCommandInteraction, member: Member
    ):
        """Hugs a user"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                data = await r.json()
                image = data["link"]
                await inter.response.send_message(
                    f"{inter.author.mention} hugged {member.mention}!!\n{image}"
                )

def setup(bot):
    bot.add_cog(Fun(bot))