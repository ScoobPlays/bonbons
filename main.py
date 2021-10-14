import discord, os, inspect, io, textwrap, traceback
from discord.ext import commands, tasks
from keep_alive import keep_alive
from contextlib import redirect_stdout

token = os.environ['token']
bot = commands.Bot(
  command_prefix=commands.when_mentioned_or('.'),
  case_insensitive=True,
  intents = discord.Intents.all(),
  allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
  strip_after_prefix=True
  )     
bot.remove_command("help")

@bot.event
async def on_ready():
  print(f'Bot is ready to be used! Ping: {round(bot.latency * 1000)}')

@tasks.loop(seconds=1000)
async def member_stats():
  guild = bot.get_guild(880030618275155998)
  online_channel = guild.get_channel(895606651728584725)

  online_members = 0

  for member in guild.members:
    if member.status == discord.Status.online:
      online_members += 1
      await online_channel.edit(name=f'Online: {online_members}')

@bot.command()
async def send(ctx, *, message:str):
  channel = bot.get_channel(897454984206118952)
  await channel.send(f"{ctx.author}: {message}")
  await ctx.message.delete()

@member_stats.before_loop
async def before_ms():
  await bot.wait_until_ready()

member_stats.start()

@bot.command(hidden=True, aliases=['eval', 'evaluate'])
@commands.is_owner()
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
    except Exception:
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

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
os.environ.setdefault('JISHAKU_NO_UNDERSCORE', '1')
os.environ.setdefault('JISHAKU_HIDE', '1')
bot.load_extension('jishaku')

if __name__ == "__main__":
