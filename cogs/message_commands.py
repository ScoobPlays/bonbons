import re

from disnake.ext import commands
from pyston import File, PystonClient


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pysclient = PystonClient()
        self.CODE_REGEX = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")

    async def run_code(self, inter, code: str):
        matches = self.CODE_REGEX.findall(str(code))
        language = matches[0][1]
        code = matches[0][2]

        output = await self.pysclient.execute(str(language), [File(code)])

        if output.raw_json["run"]["stdout"] == "" and output.raw_json["run"]["stderr"]:
            return await inter.response.send_message(
                content=f"{inter.author.mention} :warning: Your run job has completed with return code 1.\n\n```\n{output}\n```"
            )

        if output.raw_json["run"]["stdout"] == "":
            return await inter.response.send_message(
                content=f"{inter.author.mention} :warning: Your run job has completed with return code 0.\n\n```\n[No output]\n```"
            )

        else:
            return await inter.response.send_message(
                content=f"{inter.author.mention} :white_check_mark: Your run job has completed with return code 0.\n\n```\n{output}\n```"
            )

    @commands.message_command(name="Run Code")
    async def run(self, inter, message):
        await self.run_code(inter, message.content.replace(".run", ""))


def setup(bot):
    bot.add_cog(MessageCommands(bot))
