import disnake
from disnake.ext import tasks, commands
from datetime import datetime


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_tasks()

    def start_tasks(self):
        self.update_github_leaderboard.start()

    @tasks.loop(hours=2)
    async def update_github_leaderboard(self):
        
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(927523239259942972) or await self.bot.fetch_channel(
            927523239259942972
        )
        msg = await channel.fetch_message(927523690168610836)

        users = []
        async with self.bot.session.get(
            "https://api.github.com/repos/CaedenPH/Jarvide/contributors"
        ) as data:
            x = await data.json()

        for item, index in enumerate(range(11)):
            index += 1

            users.append(
                f"{index}. [`{x[item]['login']}`]({x[item]['url'].replace('api.', '').replace('users/', '')}) - {x[item]['contributions']} Commits"
            )

        embed = disnake.Embed(
            title="Top Github Contributors",
            description="\n".join(users),
            color=disnake.Color.blurple(),
            timestamp=datetime.now(),
        ).set_footer(text="Last edited at")

        await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Tasks(bot))
