import discord
from discord.ext import commands
from typing import Union
from datetime import timedelta, datetime
import random

User = Union[
    discord.Member,
    discord.User,
]

class Economy(commands.Cog, description='Economy.'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.mongo['discord']['economy']
    
    async def _create_or_find_user(self, user: User) -> dict:
        data = await self.db.find_one({'_id': user.id})

        if data is None:
            payload = {
                '_id': user.id,
                'bal': 0,
                'next_daily': None,
            }

            await self.db.insert_one(payload)
            return payload

        return data

    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx: commands.Context, user: User = None) -> None:

        """Tells you your balance."""

        user = user or ctx.author
        data = await self._create_or_find_user(user)

        embed = discord.Embed(title=f'{user.display_name}\'s Account', color=discord.Color.random())
        embed.add_field(name='Balance', value=f'{data["bal"]:,}')

        await ctx.send(embed=embed)

    @commands.command(name='daily')
    async def daily(self, ctx: commands.Context) -> None:
            
        """Gives you your daily money."""
    
        user = ctx.author
        data = await self._create_or_find_user(user)
        next_daily = (datetime.now() + timedelta(days=1)).timestamp()
    
        if data['next_daily'] is None or data['next_daily'] <= int(datetime.now().timestamp()):

            data['bal'] += 100
            data['next_daily'] = int(next_daily)

            await self.db.update_one({'_id': user.id}, {'$set': data})
            return await ctx.send(f'{user.mention} Here is your daily 💰!')

        await ctx.send(f'{user.mention} You already claimed your daily 💰!')



    @commands.command(name='work')
    async def work(self, ctx: commands.Context) -> None:

        user = ctx.author
        data = await self._create_or_find_user(user)
        coins = random.randint(25, 250)

        data['bal'] += coins

        await self.db.update_one({'_id': user.id}, {'$inc': {'bal': coins}})
        await ctx.send(f'{user.mention} You worked and got {coins} 💰!')



def setup(bot: commands.Bot) -> None:
    bot.add_cog(Economy(bot))
