import disnake
from disnake.ext import commands
import os
import datetime
from aiohttp import ClientSession
from keep_alive import keep_alive

bot = commands.Bot(
    command_prefix=".",
    test_guilds=[880030618275155998],
    case_insensitive=True,
    intents=disnake.Intents.all(),
    allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False),
    help_command=None,
    strip_after_prefix=True,
    status=disnake.Status.dnd,
    activity=disnake.Game(name="/ commands (soon)"),
)


@bot.event
async def on_ready():
    print(f"Bot is ready to be used! Ping: {round(bot.latency * 1000)}")
    if not hasattr(bot, "session"):
        bot.session = ClientSession(loop=bot.loop)


# https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96#gistcomment-3623975
# https://mystb.in/EthicalBasketballPoliticians.python


class HelpEmbed(disnake.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [category] for more information"
        self.set_footer(text=text)
        self.color = disnake.Color.blurple()


class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={"hidden": True, "aliases": ["commands"]})

    async def send(self, **kwargs):
        """a short cut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        """triggers when a `<prefix>help` is called"""
        ctx = self.context
        embed = HelpEmbed(title="Help Menu")
        usable = 0

        for (
            cog,
            commands,
        ) in mapping.items():  # iterating through our mapping of cog: commands
            if filtered_commands := await self.filter_commands(commands):
                # if no commands are usable in this category, we don't want to display it
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:  # getting attributes dependent on if a cog exists or not
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No Category"
                    description = "Commands with no category"

                embed.add_field(
                    name=f"{name} Category [{amount_commands}]", value=description
                )

        embed.description = f"{len(bot.commands)} commands | {usable} usable"

        await self.send(embed=embed)

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        signature = self.get_command_signature(
            command
        )  # get_command_signature gets the signature of a command in <required> [optional]
        embed = HelpEmbed(
            title=signature, description=command.help or "No help found..."
        )

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        can_run = "No"
        # command.can_run to test if the cog is usable
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"

        embed.add_field(name="Usable", value=can_run)

        if command._buckets and (
            cooldown := command._buckets._cooldown
        ):  # use of internals to get the cooldown of the command
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await self.send(embed=embed)

    async def send_help_embed(
        self, title, description, commands
    ):  # a helper function to add commands to an embed
        embed = HelpEmbed(title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.help or "No help found...",
                )

        await self.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(
            f"{title} Category", cog.description, cog.get_commands()
        )


bot.help_command = MyHelp()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


keep_alive()
os.environ["JISHAKU_FORCE_PAGINATOR"] = "1"
os.environ["JISHAKU_EMBEDDED_JSK"] = "1"
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")
os.environ.setdefault("JISHAKU_HIDE", "1")
bot.load_extension("jishaku")

if __name__ == "__main__":
    bot.run(os.environ["token"])
