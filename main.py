import discord 
import os
from discord.ext import commands
from datetime import datetime
from keep_alive import keep_alive
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout

# gold = #fff1b6
# light_blue = #96daff

token = os.environ['token']
bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), case_insensitive=True, intents = discord.Intents.all(), allowed_mentions=discord.AllowedMentions(everyone=False))

@bot.event
async def on_ready():
  print(f'Bot is ready to be used! Ping: {round(bot.latency * 1000)}')
  await bot.change_presence(status=discord.Status.dnd)

  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
      destination = self.get_destination()
      for page in self.paginator.pages:
        embed = discord.Embed(description=page)
        embed.timestamp=datetime.utcnow()
        embed.set_author(name=self.context.author, icon_url=self.context.author.display_avatar)
        embed.set_footer(text='Minimal Help Command', icon_url=self.context.author.display_avatar)
        await destination.send(embed=embed)
    
    async def send_command_help(self, command):
      embed = discord.Embed(title=self.get_command_signature(command))
      command_has_alias = command.aliases
      command_has_help = command.help
      if command_has_help:
        embed.add_field(name="Help", value=command.help)
      if command_has_alias:
        embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)

      channel = self.get_destination()
      await channel.send(embed=embed)
    
    async def send_error_message(self, error):
      embed = discord.Embed(title="Error", description=error)
      channel = self.get_destination()
      await channel.send(embed=embed)

@bot.command(aliases=['eval', 'evaluate'])
async def run(ctx, *, code):
    """Evaluates python code."""
    env = {
        'ctx': ctx,
        'bot': bot,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        'source': inspect.getsource
    }
 
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
 
        # remove `foo`
        return content.strip('` \n')
 
    def get_syntax_error(e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'
 
    env.update(globals())
 
    code = cleanup_code(code)
    stdout = io.StringIO()
    err = out = None
 
    to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
 
    def paginate(text: str):
        '''Simple generator that paginates text.'''
        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text)-1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != '', pages))
 
    try:
        exec(to_compile, env)
    except Exception as e:
        err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        return await ctx.message.add_reaction('\u2049')
 
    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        if ret is None:
            if value:
                try:
 
                    out = await ctx.send(f'```py\n{value}\n```')
                except:
                    paginated_text = paginate(value)
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')
        else:
            try:
                out = await ctx.send(f'```py\n{value}{ret}\n```')
            except:
                paginated_text = paginate(f"{value}{ret}")
                for page in paginated_text:
                    if page == paginated_text[-1]:
                        out = await ctx.send(f'```py\n{page}\n```')
                        break
                    await ctx.send(f'```py\n{page}\n```')
 
    if out:
        await ctx.message.add_reaction('\u2705')  # tick
    elif err:
        await ctx.message.add_reaction('\u2049')  # x
    else:
        await ctx.message.add_reaction('\u2705')

bot.help_command = MyNewHelp()
keep_alive()
os.environ.setdefault('JISHAKU_NO_UNDERSCORE', '1')
os.environ.setdefault('JISHAKU_HIDE', '1')
bot.load_extension('jishaku')
bot.run(token)
