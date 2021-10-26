import disnake
from disnake.ext import commands
import base64

#def binary(text: str):
#  return (" ".join(f"{ord(i):08b}" for i in text))

#https://www.rapidtables.com/convert/number/binary-to-ascii.html

class Translation(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.group()
    async def base64(self, ctx: commands.Context):
      pass

    @base64.command()
    async def encode(self, ctx: commands.Context, *, text: str):
        """Encodes a message"""
        try:
          message_bytes = text.encode("ascii")
          base64_bytes = base64.b64encode(message_bytes)
          base64_message = base64_bytes.decode("ascii")
      
          await ctx.reply(base64_message, mention_author=False)
        except Exception:
          await ctx.reply(f"Couldn't encode that message.", mention_author=False)

    @base64.command()
    async def decode(self, ctx: commands.Context, *, body:str):
        """Decodes base64"""
        try:
          base64_bytes = body.encode("ascii")
          message_bytes = base64.b64decode(base64_bytes)
          message = message_bytes.decode("ascii")
          
          await ctx.reply(message, mention_author=False)
        except Exception:
          await ctx.reply("Couldn't decode that message.", mention_author=False)

def setup(bot):
  bot.add_cog(Translation(bot))
