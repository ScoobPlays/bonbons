import discord
from discord.ext import commands
from typing import Union
from datetime import timedelta, datetime
import random
import json

User = Union[
    discord.Member,
    discord.User,
]

class Economy(commands.Cog, description='Economy.'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.mongo['discord']['economy']

        with open('utils/database/shop.jsonc', 'r') as _shop:
            self._shop = json.load(_shop)
    
    async def _create_or_find_user(self, user: User) -> dict:
        data = await self.db.find_one({'_id': user.id})

        if data is None:
            payload = {
                '_id': user.id,
                'balance': 0,
                'inventory': [],
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
        embed.description = f'**Balance**: {data["balance"]:,}'

        await ctx.send(embed=embed)

    @commands.command(name='daily')
    async def daily(self, ctx: commands.Context) -> None:
            
        """Gives you your daily $$$!"""
    
        user = ctx.author
        data = await self._create_or_find_user(user)
        next_daily = (datetime.now() + timedelta(days=1)).timestamp()
    
        if data['next_daily'] is None or data['next_daily'] <= int(datetime.now().timestamp()):

            data['balance'] += 100
            data['next_daily'] = int(next_daily)

            await self.db.update_one({'_id': user.id}, {'$set': data})
            return await ctx.send(f'{user.mention} Here is your daily 💰!')

        await ctx.send(f'{user.mention} You already claimed your daily 💰!')


    @commands.command(name='work')
    async def work(self, ctx: commands.Context) -> None:

        """Work for some extra cash!"""

        user = ctx.author
        data = await self._create_or_find_user(user)
        coins = random.randint(25, 250)

        data['bal'] += coins

        await self.db.update_one({'_id': user.id}, {'$inc': {'balance': coins}})
        await ctx.send(f'{user.mention} You worked and got {coins} 💰!')

    @commands.command(name='shop')
    async def shop(self, ctx: commands.Context) -> None:
            
        """Shows you the shop."""

        embed = discord.Embed(title=f'Shop', color=discord.Color.random(), description='')
        embed.set_thumbnail(url=self.bot.user.display_avatar)

        for key in self._shop.keys():

            base = self._shop[key]
            embed.description += f'\n**{base["name"]}** -- {base["price"]:,} 💰\n{base["description"]}'

        await ctx.send(embed=embed)

    @commands.command(name='buy')
    async def buy(self, ctx: commands.Context, item: str) -> None:
                
        """Buy an item from the shop."""

        user = ctx.author
        data = await self._create_or_find_user(user)
        item = self._shop[item]

        if data['balance'] >= item['price']:
            data['balance'] -= item['price']
            data['inventory'].append(item['name'])

            await self.db.update_one({'_id': user.id}, {'$set': data})
            return await ctx.send(f'{user.mention} You bought **{item["name"]}** for {item["price"]:,} 💰!')

        await ctx.send(f'{user.mention} You don\'t have enough 💰 to buy this item!')


    @commands.command(name='inventory', aliases=['inv'])
    async def inventory(self, ctx: commands.Context) -> None:
                
        """Shows you your inventory."""
        
        user = ctx.author
        data = await self._create_or_find_user(user)

        if len(data['inventory']) == 0:
            return await ctx.send(f'{user.mention} You don\'t have any items!')
    
        embed = discord.Embed(title=f'{user.display_name}\'s Inventory', color=discord.Color.random())
        embed.description = '\n'.join(data['inventory']) # TODO: parse items if the user has multiple of the same item
    
        await ctx.send(embed=embed)



def setup(bot: commands.Bot) -> None:
    bot.add_cog(Economy(bot))
