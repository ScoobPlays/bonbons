import disnake
from disnake.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.logs = self.bot.get_guild(880030618275155998).get_channel(907820956733558784)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        
        embed = disnake.Embed(
            title="Message Deleted",
            description=f"""
            **Author:** {message.author.mention} ({message.author.id})
            **Guild:** {message.guild.name} ({message.guild.id})
            **Channel:** {message.channel.mention} ({message.channel.id})
            **Deleted At:** <t:{int(message.created_at.timestamp())}:F> (<t:{int(message.created_at.timestamp())}:R>)
            """
        ).add_field(
            name="Message Content",
            value=message.content
        )
        await self.logs.send(embed=embed)

def setup(bot):
    bot.add_cog(Logs(bot))