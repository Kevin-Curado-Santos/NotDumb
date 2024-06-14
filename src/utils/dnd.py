import discord 
import random

from discord.ext import commands

def roll_multiple(expr):
    [num, dice] = expr.split('d')

    return [random.randint(1, int(dice)) for _ in range(int(num) if num != '' else 1)]

class Dndbot(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def roll(self, ctx, *, expr = None):
        if expr == None:
            roll = random.randint(1, 20)
            if roll == 1 or roll == 20:
                embedVar = discord.Embed(title=f'{"Unlucky!" if roll == 1 else "Lucky!"}', color=0x00ff00)
                embedVar.add_field(name=f'You rolled a nat `{roll}`', value='')
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title='d20 Roll', color=discord.Color.random())
                embedVar.add_field(name=f'You rolled a `{roll}`', value='')
                await ctx.send(embed=embedVar)
        else:
            results = roll_multiple(expr)

            embedVar = discord.Embed(title=f'{expr} roll', color=discord.Color.random())
            embedVar.add_field(name=f'You rolled {sum(results)}', value='+'.join(map(str, results)))
            await ctx.send(embed=embedVar)



